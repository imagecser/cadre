# -*- coding: utf-8 -*-
"""
Created by suun on 5/4/2018
"""
from Cadre import pybloom
from Cadre import items
from Cadre import utils
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


class DefaultSpider(object):
    name = "default"
    start_urls = ['https://www.icser.me']
    allowed_domains = ['icser.me']
    banned_domains = ['img.icser.me']
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
        self.logger = utils.get_logger("Cadre.spider")

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

    @staticmethod
    def get_url(url, base_url):  # specified method
        if not url.startswith('http'):
            if not url.startswith('/'):
                url = '/' + url
            url = base_url + url
        return url

    @staticmethod
    def process_text(text):  # specified method
        # text = re.compile("(<script[^>]*>[^<]+</script>|"
        #                   "<style[^>]*>[^<]+</style>)", re.S).sub("", text)  # 去除script
        # text = re.compile("<[^>]*>", re.S).sub(" ", text)  # 去除所有的标签
        # text = re.compile("&[^;]+;", re.S).sub(" ", text)  # 去除特殊字符
        # text = re.compile("[A-~0-9!-@]+", re.S).sub(" ", text)  # 去除英文字符
        # text = re.compile("\s+", re.S).sub(" ", text)  # 去除多余的blank

        return ' '.join(re.compile("[\u4e00-\u9fa5]+").findall(text))

    def jw_parse(self, response):  # specified method
        self.logger.info("on jw_parse")

    def start_requests(self):  # to be override
        for url in self.start_urls:
            self.to_request(None, url)

    def err_parse(self, url, err):  # to be override
        self.logger.error("scraped from %s: %s" % (url, err))

    def parse(self, response):  # to be override
        if 'text/html' not in response.headers['content-type']:
            return items.DefaultItem({'url': '', 'content': ''})
        cur_url = response.url
        # self.logger.debug("parsing from: %s" % cur_url)
        text = response.content.decode('utf-8', 'ignore')
        item = items.DefaultItem()
        item['url'] = cur_url
        item['content'] = self.process_text(text)

        base_url = re.compile("https?://[^/]*").match(cur_url).group()
        tar_urls = re.compile("<a[^>]*href=\"[^\"]*\"[^>]*>").findall(text)
        tar_urls = [self.get_url(re.compile("href=\"([^\"]*)\"").findall(url)[0],
                                 base_url) for url in tar_urls]
        for url in tar_urls:
            self.to_request(cur_url, url)

        return item
        # print(list(map(lambda _url: self.get_url(_url, base_url), tar_urls)))
        # logging.error(str(tar_urls))

# thread_parse = []
# for i in range(20):
#     thread_parse.append(threading.Thread(target=parse_page, name="parse"))
# for t in thread_parse:
#     t.start()
# for t in thread_parse:
#     t.join()
# multiple threadings
