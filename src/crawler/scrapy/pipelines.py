# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        # print('DoubanbookPipeline')
        # print(item)
        print('DoubanbookPipeline:' + item['title'] + ' | ' + item['rate'] + ' | ' + item['author'])
        return item
