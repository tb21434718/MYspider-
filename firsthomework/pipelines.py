# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests

class FirsthomeworkPipeline(object):
    def process_item(self, item, spider):
        ''' 处理每一个传过来的item'''
        # 获取当前工作目录
        base_dir = os.getcwd()
        # 文件存在data目录下的weather.txt文件内
        filename = base_dir + '\\nuaa.csv'
        print(filename)
        # 从内存以追加的方式打开文件，并写入对应的数据

        with open(filename,'a',encoding='utf-8') as f:
            f.write('姓名:'+item['teachername'] + '\n')
            f.write('学位:' + item['degree'] + '\n')
            f.write('年龄:' + item['age'] + '\n')
            f.write('学院:' + item['college'] + '\n')
            f.write('职称:'+item['technicalpost'] + '\n')
            f.write('研究方向:'+item['researchdirection'] + '\n')
            f.write('Email:'+item['email'] + '\n\n')
        return item