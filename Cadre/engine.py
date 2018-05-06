# -*- coding: utf-8 -*-
"""
Created by suun on 5/5/2018
"""

from spider import DefaultSpider
from pipeline import DefaultPipeLine
import utils
import threading
import time
import queue


class Engine(object):
    def __init__(self, con_requests=1, con_items=1):
        self.spider = DefaultSpider()
        self.pipeline = DefaultPipeLine()
        self.request_threads = []
        self.pipe_threads = []

        self.doing_request = -1
        self.doing_lock = threading.Lock()
        self.logger = utils.get_logger("Cadre.engine")
        for i in range(con_requests):
            self.request_threads.append(threading.Thread(
                target=self.request, name="request_%d" % i, args=()))
        for i in range(con_items):
            self.pipe_threads.append(threading.Thread(
                target=self.pipe, name="pipe_%d" % i, args=()))

    def open_spider(self):
        self.spider.start_requests()
        self.pipeline.open_spider(self.spider)

    def close_spider(self):
        self.pipeline.close_spider(self.spider)

    def over_request(self):
        if self.spider.cache.empty():
            with self.doing_lock:
                if self.doing_request == -1:
                    self.doing_request = 0
                elif self.doing_request == 0:
                    return True
        return False

    def request(self):
        while True:
            if self.over_request():
                self.logger.debug("%s stopped" % threading.current_thread())
                break
            try:
                referer, url = self.spider.cache.get(timeout=3)
            except queue.Empty:
                continue
            with self.doing_lock:
                self.doing_request += 1
            ret = self.spider.request(referer, url)
            with self.doing_lock:
                self.doing_request -= 1
            if ret:
                self.pipeline.cache.put(ret)
                # self.logger.debug("engine.pipeline.cache "
                #                   "has %d item" % self.pipeline.cache.qsize())

    def pipe(self):
        while True:
            if self.pipeline.cache.empty():
                if self.over_request():
                    self.logger.debug("%s stopped" % threading.current_thread())
                    break
            try:
                item = self.pipeline.cache.get(timeout=3)
            except queue.Empty:
                continue
            self.pipeline.process_item(self.spider, item)

    def execute_spider(self):
        for t in self.request_threads:
            t.start()
        time.sleep(1)
        for t in self.pipe_threads:
            t.start()
        for t in (self.request_threads + self.pipe_threads):
            t.join()

    def stop_request(self):
        for t in self.request_threads:
            t.stop()

    def stop_pipe(self):
        for t in self.pipe_threads:
            t.stop()


if __name__ == '__main__':
    engine = Engine()
    engine.open_spider()
    engine.execute_spider()
    engine.close_spider()
