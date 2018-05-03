# -*- coding: utf-8 -*-
import scrapy
import NJUSpider.items
from twisted.internet import error
import re
import pybloom


def decorator(func):
    def wrapper(cls, response, *args, **kwargs):
        # cls.count += 1
        # if cls.count % 100 == 1:
        #     log.msg("scraped %d pages." % cls.count, _level=log.DEBUG)
        if 'text/html' not in response.headers['Content-Type'].decode():
            return
        return func(cls, response, *args, **kwargs)
    return wrapper


class NjuSpider(scrapy.Spider):
    name = 'nju'
    allowed_domains = ['nju.edu.cn']
    banned_domains = ['lmswe.nju.edu.cn', 'im.nju.edu.cn',
                      'stuex.nju.edu.cn/en', 'lamda.nju.edu.cn', 'GFS.asp']
    start_urls = ['http://news.nju.edu.cn/index.html']
    invalid_ends = ['pdf', 'doc', 'docx', 'wps', 'xls', 'xlsx', 'rar', 'zip', 'exe', 'tar',
                    'png', 'jpg', 'jpeg', 'bmp', 'swf', '7z', 'iso', 'gz', 'tar', 'ppt']

    def __init__(self):
        self.scrawled_urls = pybloom.BloomFilter(n=100000)
        # self.count = 0

    @staticmethod
    def get_text(content):
        content = re.compile("<script.*script>", re.S).sub("", content)
        content = re.compile("<[^>]*>").sub("", content)
        content = re.compile("[\t\r\n ]+").sub(" ", content)
        return content

    @staticmethod
    def get_url(url, base_url):
        if not url.startswith('http'):
            if not url.startswith('/'):
                url = '/' + url
            url = base_url + url
        return url

    def filter_request(self, url, *args, **kwargs):
        if url not in self.scrawled_urls:
            self.scrawled_urls.add(url)
            for banned_url in NjuSpider.banned_domains:
                if banned_url in url:
                    return
            for end in NjuSpider.invalid_ends:
                if url.endswith(end):
                    return
            return scrapy.Request(url, *args, **kwargs)

    @decorator
    def parse(self, response):
        item = NJUSpider.items.NjuspiderItem()
        item['url'] = response.request.url
        body_content = response.xpath("body").extract_first()
        try:
            item['content'] = self.get_text(body_content)
        except TypeError:
            return
        yield item

        base_url = re.compile("https?://[^/]*").match(item['url']).group()
        tar_urls = list(map(lambda tar: tar[6:-1],
                            response.xpath("//a[@href]").re("href=\"[^\"]*\"")))
        for url in tar_urls:
            url = self.get_url(url, base_url)
            # self.logger.debug("get href: %s." % url)
            yield self.filter_request(url, callback=self.parse, errback=self.err_parse)

    def err_parse(self, failure):
        # if failure.check(error.TimeoutError):
        #     request = failure.request
        #     self.logger.error('TimeoutError on %s.' % request.url)
        # else:
        #     self.logger.error(repr(failure))
        self.logger.error(repr(failure) + failure.request.url)
