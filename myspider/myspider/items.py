# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #超市名称
    name = scrapy.Field()
    #超市地址
    address = scrapy.Field()
    #超市电话
    phone = scrapy.Field()

