# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import log
from scrapy import signals
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random


class NjuSpiderUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent='Mozilla/5.0 (compatible;'
                                  ' Googlebot/2.1; +http://www.google.com/bot.html)'):
        self.user_agent = user_agent
        self.user_agent_list = [
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 "
            "Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) "
            "AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 "
            "Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Googlebot/2.1; startmebot/1.0; +https://start.me/bot)",
            "Googlebot/2.1 (+http://www.googlebot.com/bot.html)",
            "Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; "
            "Google Page Speed Insights) Chrome/27.0.1453 Safari/537.36 GoogleBot/2.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/537.36 "
            "(KHTML, like Gecko; Google Page Speed Insights) "
            "Version/6.0 Mobile/10A525 Safari/8536.25 GoogleBot/2.1",
            "Mozilla/5.0 (compatible; Googlebot/2.1; http://www.google.com/bot.html)",
            "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; Google Web "
            "Preview Analytics) Chrome/27.0.1453 Safari/537.36 (compatible; "
            "Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible;acapbot/0.1;treat like Googlebot)",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://import.io)",
            "Google Crawler: Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko;"
            " Google Web Preview Analytics) Chrome/41.0.2272.118 Safari/537.36"
            " (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "OnPageBot (compatible; Googlebot 2.1; +https://bot.onpage.org/)",
            "Mozilla/5.0 (compatible; Googlebot/2.1 +http://www.googlebot.com/bot.html)",
            "Mozilla/5.0 (compatible;acapbot/0.1.;treat like Googlebot)",
            "Googlebot/2.1; +http://www.google.com/bot.html)"
        ]

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        request.headers.setdefault('User-Agent', ua)


class NjuspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NjuspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
