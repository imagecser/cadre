# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class NjuspiderPipeline(object):
    def open_spider(self, spider):
        self.fjson = codecs.open("res.json", "w", encoding="utf-8")

    def close_spider(self, spider):
        self.fjson.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.fjson.write(line)
        return ''
