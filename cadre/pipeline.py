# -*- coding: utf-8 -*-
"""
Created by suun on 5/5/2018
"""

from cadre import utils
import queue


class PipeLine(object):
    def __init__(self):
        self.logger = utils.get_logger("cadre.pipeline")
        self.cache = queue.Queue()

    def open_spider(self):
        """
        do before spider open
        """

    def close_spider(self):
        """
        do after spider close
        """

    def process(self, url, item):
        self.logger.debug("Piped from <%s>" % url)
        self.process_item(item)

    def __del__(self):
        self.close_spider()

    def process_item(self, item):
        """
        process item from spider.parse
        """
        return item


class DefaultPipeline(PipeLine):
    """
    default pipeline
    """
