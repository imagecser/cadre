# -*- coding: utf-8 -*-
"""
Created by suun on 5/5/2018
"""

from Cadre import utils
import queue
import codecs
import json


class DefaultPipeLine(object):
    def __init__(self):
        self.logger = utils.get_logger("Cadre.pipeline")
        self.cache = queue.Queue()

    def open_spider(self, spider):
        self.fh = codecs.open("res.json", "w", encoding='utf-8')
        """
        do before spider open
        """

    def close_spider(self, spider):
        self.fh.close()
        """
        do after spider close
        """

    def process(self, spider, url, item):
        self.logger.debug("Saved from <%s>" % url)
        self.process_item(spider, item)

    def process_item(self, spider, item):
        """
        process item from spider.parse
        """
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.fh.write(line)
        return item
