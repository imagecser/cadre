# -*- coding: utf-8 -*-
"""
Created by suun on 5/5/2018
"""
import utils
import queue


class DefaultPipeLine(object):
    def __init__(self):
        self.logger = utils.get_logger("pipeline")
        self.cache = queue.Queue()

    def open_spider(self, spider):
        """
        do before spider open
        """

    def close_spider(self, spider):
        """
        do after spider close
        """

    def process_item(self, spider, item):
        """
        process item from spider.parse
        """
        print("{url}: {desc}...".format(url=item['url'], desc=item['content'][:20]))
