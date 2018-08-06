# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from myspider.items import *
# from myspider.spiders.city_all import city
import re


city = input('请输入城市名称：')
class SortesSpider(CrawlSpider):
    name = 'sortes'
    allowed_domains = ['poi.mapbar.com']

    # start_urls = ['http://poi.mapbar.com/beijing/520/']
    # url = 'http://poi.mapbar.com/{}/520/'
    # city = input('请输入城市名称：')
    # 自己定制配置文件中的某些选项
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         # 'movieproject.pipelines.MyMongoDbPipeline': 302,
    #         'scrapy_redis.pipelines.RedisPipeline': 400,
    #     }
    # }
    #按照需要爬取得城市名称爬取超市信息
    def start_requests(self):
        
        url_start = 'http://poi.mapbar.com/{}/520/'.format(city)
        yield scrapy.Request(url=url_start,callback=self.parse)


    def parse(self, response):
        #获取一级href
        div_list = response.xpath('//div[@class="sort cl"]//dl/dd/a/@href').extract()

        #遍历所有链接
        for _list in div_list:
            yield scrapy.Request(url=str(_list),callback=self.parse_detail)

    def parse_detail(self,response):

        #定义item
        item = MyspiderItem()
        # 超市名称
        item['name'] = response.xpath('//h1[@id="poiName"]/text()').extract_first()

        #市
        address1 = response.xpath('//div[@class="infoPhoto"]//ul/li[2]/a[1]/text()')[0].extract()
        #区
        address2 = response.xpath('//div[@class="infoPhoto"]//ul/li[2]/a[2]/text()')[0].extract()
        # 超市具体地址
        address3 = response.xpath('//div[@class="infoPhoto"]//ul/li[2]/text()')[3].extract()
        # 超市电话
        phone = response.xpath('//div[@class="infoPhoto"]//ul/li[3]/text()')[1].extract()
        c = re.compile(r'\s')
        yu = re.compile(r'，')
        phonee = yu.sub('', phone)
        phone = c.sub('', phonee)
        if phone != '无':
            #匹配空格、换行符，
            c = re.compile(r'\s')
            #空格、换行符更改为空
            address = c.sub('',address3)

            if address.find('省') == -1:
                item['address'] = address1 + ' ' + address2 +''+ address
                item['phone'] = phone
                yield item

            else:
                #如果带有省字   省字切割 取第一段字符
                addre = address.split('省')
                #地址以 省、市、区街道  将切割后的省字添加到addre
                addres = addre[0] + '省'
                #匹配省字
                c = re.compile(r'省')
                #切割后取 第二段字符 将省字去掉
                _address = c.sub('', addre[-1])
                #拼接省、市、地区详细地址
                item['address'] = addres +' '+ address1 + ' ' + _address
                item['phone'] = phone
                yield item








