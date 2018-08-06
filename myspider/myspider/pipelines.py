# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy.utils.project import get_project_settings
from myspider.spiders.sortes import city
class MyspiderPipeline(object):
    def open_spider(self,spider):
        #链接数据库
        # 将配置文件读到内存中，是一个字典
        settings = get_project_settings()
        host = settings['DB_HOST']
        port = settings['DB_PORT']
        user = settings['DB_USER']
        password = settings['DB_PASSWORD']
        dbname = settings['DB_NAME']
        dbcharset = settings['DB_CHARSET']

        self.conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=dbname, charset=dbcharset)

    def process_item(self,item,spider):

        #创建数据库表，填写id  name address  phone
#判断是否存在，存在的则跳过， if not exists
        sq = 'create table  if not exists {table_name}(id int auto_increment,primary key(id), name varchar(200), address varchar(1000), phone varchar(30))engine=innodb default charset=utf8;'.format(table_name = city)


        # 写入数据库中
        sql = 'insert into {table_name}(name,address,phone) values("%s","%s", "%s")'.format(table_name=city) % (
        item['name'], item['address'], item['phone'])
        # 执行sql语句
        self.cursor = self.conn.cursor()
        self.cursor.execute(sq)
        try:
            self.cursor.execute(sql)
            print('写入中...')
            self.conn.commit()
        except Exception as e:
            print('错误！')
            print(e)
            self.conn.rollback()

        return item
