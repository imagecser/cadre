# -*- coding: utf-8 -*-
"""
Created by suun on 5/4/2018
"""
import pybloom
from cadre import items
from cadre import utils
import re
import requests
import queue
import time
import threading

lock_count = threading.Lock()


# def decorator(call):
#     def in_decorator(func):
#         def wrapper(*args, **kwargs):
#             call(*args, **kwargs)
#             return func(*args, **kwargs)
#         return wrapper
#     return in_decorator


class Spider(object):
    name = "default"
    start_urls = []
    allowed_domains = []
    banned_domains = []
    invalid_extensions = []
    invalid_protocols = []
    rules = {
        # r"jw.nju.edu.cn": "jw_parse"
    }  # must be regular expression

    def __init__(self, n=10000):
        self.count = 0
        self.max_size = 100
        self.cache = queue.Queue(0)
        self.pageset = pybloom.BloomFilter(n)
        self.lock = threading.Lock()
        self.url_header = {
            'User-Agent': 'Mozilla/5.0 (compatible; '
                          'Googlebot/2.1; +http://www.google.com/bot.html)',
            'Proxy-Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-SG,zh;q=0.9,zh-CN;q=0.8,en;q=0.7,zh-TW;q=0.6'
        }
        self.start_time = time.time()
        self.logger = utils.get_logger("cadre.spider")
        self.open_spider()

    def to_request(self, referer, url):
        if url not in self.pageset:
            for banned_url in self.banned_domains:
                if banned_url in url:
                    return
            if len(self.allowed_domains):
                for allowed_url in self.allowed_domains:
                    if allowed_url not in url:
                        return
            for extension in self.invalid_extensions:
                if url.endswith(extension):
                    return
            for protocol in self.invalid_protocols:
                if url.startswith(protocol):
                    return
            self.pageset.add(url)
            self.cache.put((referer, url))

    def request(self, prev, url):
        with self.lock:
            self.count += 1
        sub_header = self.url_header
        sub_header['Host'] = re.compile("^https?://([^/]*).*").sub(r'\1', url)
        sub_header['Referer'] = prev
        try:
            response = requests.get(url, headers=sub_header, timeout=15)
        except Exception as err:
            return self.err_parse(url, err)
        self.logger.debug("Crawled ({status}) <{url}>".format(
            status=response.status_code, url=url))
        for rule, attr in self.rules.items():
            if re.compile(rule).search(url):
                return getattr(self, attr)(response)
        return self.parse(response)

    def open_spider(self):
        for url in self.start_urls:
            self.to_request(None, url)
        self.start_requests()

    def start_requests(self):  # to be override
        """
        """

    def err_parse(self, url, err):  # to be override
        self.logger.error("scraped from %s: %s" % (url, err))

    def parse(self, response):  # to be override
        item = items.DefaultItem()
        item['content'] = response.content.decode('utf-8', 'ignore')
        return item


class DefaultSpider(Spider):
    """
    default spider
    """
