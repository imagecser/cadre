# -*- coding: utf-8 -*-
"""
Created by suun on 5/5/2018
"""

from Cadre.spider import DefaultSpider
from Cadre.pipeline import DefaultPipeLine
from Cadre import utils
import threading
import queue


class SharedData(object):
    def __init__(self, spider, pipeline):
        self.spider = spider
        self.pipeline = pipeline
        self.doing_request = -1
        self.doing_lock = threading.Lock()


class RequestThread(threading.Thread):
    def __init__(self, shared, thread_name):
        super(RequestThread, self).__init__(name=thread_name)
        self.logger = utils.get_logger("Cadre.engine.%s" % thread_name)
        self.logger.propagate = False
        self.shared = shared

    def run(self):
        while True:
            if self.shared.spider.cache.empty() and self.shared.doing_request == 0:
                self.logger.debug("%s stopped" % threading.current_thread())
                break
            try:
                referer, url = self.shared.spider.cache.get(timeout=1)
            except queue.Empty:
                continue
            with self.shared.doing_lock:
                self.shared.doing_request = max(self.shared.doing_request + 1, 1)
            ret = self.shared.spider.request(referer, url)
            with self.shared.doing_lock:
                self.shared.doing_request -= 1
            if ret:
                self.shared.pipeline.cache.put((url, ret))


class PipeThread(threading.Thread):
    def __init__(self, shared, thread_name):
        super(PipeThread, self).__init__(name=thread_name)
        self.logger = utils.get_logger("Cadre.engine.%s" % thread_name)
        self.logger.propagate = False
        self.shared = shared

    def run(self):
        while True:
            if self.shared.pipeline.cache.empty():
                if self.shared.spider.cache.empty() and self.shared.doing_request == 0:
                    self.logger.debug("%s stopped" % threading.current_thread())
                    break
            try:
                url, item = self.shared.pipeline.cache.get(timeout=1)
            except queue.Empty:
                continue
            self.shared.pipeline.process(self.shared.spider, url, item)


class Engine(object):
    def __init__(self, con_requests=10, con_items=1):
        self.spider = DefaultSpider()
        self.pipeline = DefaultPipeLine()
        self.shared = SharedData(self.spider, self.pipeline)
        self.logger = utils.get_logger("Cadre.engine")

        self.request_threads = []
        self.pipe_threads = []
        for i in range(con_requests):
            self.request_threads.append(RequestThread(self.shared, "request%d" % i))
        for i in range(con_items):
            self.pipe_threads.append(PipeThread(self.shared, "pipe%d" % i))

        self.open_spider()

    def open_spider(self):
        self.spider.start_requests()
        self.pipeline.open_spider(self.spider)

    def close_spider(self):
        self.pipeline.close_spider(self.spider)

    def __del__(self):
        self.close_spider()

    def execute_spider(self):
        for t in (self.request_threads + self.pipe_threads):
            t.start()
        for t in (self.request_threads + self.pipe_threads):
            t.join()
        self.logger.debug("MainThread returned")

    def stop_request(self):
        for t in self.request_threads:
            t.stop()

    def stop_pipe(self):
        for t in self.pipe_threads:
            t.stop()


engine = Engine()
engine.execute_spider()
