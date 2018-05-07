# -*- coding: utf-8 -*-
"""
Created by suun on 5/7/2018
"""
from cadre import spider
from . import items
import re


class NjuSpider(spider.DefaultSpider):
    name = 'nju'
    start_urls = ['https://www.icser.me']
    allowed_domains = ['icser.me']
    invalid_extensions = ['jpg']

    @staticmethod
    def get_url(url, base_url):  # specified method
        if not url.startswith('http'):
            if not url.startswith('/'):
                url = '/' + url
            url = base_url + url
        return url

    def parse(self, response):  # to be override
        if 'text/html' not in response.headers['content-type']:
            return items.NjuItem({'url': '', 'content': ''})
        cur_url = response.url
        # self.logger.debug("parsing from: %s" % cur_url)
        text = response.content.decode('utf-8', 'ignore')
        item = items.NjuItem()
        item['url'] = cur_url
        item['content'] = ' '.join(re.compile("[\u4e00-\u9fa5]+").findall(text))

        base_url = re.compile("https?://[^/]*").match(cur_url).group()
        tar_urls = re.compile("<a[^>]*href=\"[^\"]*\"[^>]*>").findall(text)
        tar_urls = [self.get_url(re.compile("href=\"([^\"]*)\"").findall(url)[0],
                                 base_url) for url in tar_urls]
        for url in tar_urls:
            self.to_request(cur_url, url)
        return item
