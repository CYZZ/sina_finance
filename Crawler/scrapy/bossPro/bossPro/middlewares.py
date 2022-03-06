# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BossproSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
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


class BossproDownloaderMiddleware:
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
        # request.cookies = {
        #     "lastCity": "101020100",
        #     "acw_tc": "0bdd344e16461439102167283e1749b8f193004c617fe8d55570a98b2363f1",
        #     "__zp_seo_uuid__": "d788d105-a08c-4808-a726-d2cb530c4358",
        #     "__g": "-",
        #     "__l": "r=https://www.baidu.com/link?url=CzW5cDw4HaG3tQkhkgSL_ESym_NbSU374zWzz6AGad5m2AyUfwLTw-QXOF-U92by&wd=&eqid=834ac673000cf1b700000003621e299f&l=/www.zhipin.com/shanghai/&s=1&g=&s=3&friend_source=0",
        #     "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1646141408,1646142483,1646143916",
        #     "__c": "1646141408",
        #     "__a": "16771029.1646141408..1646141408.11.1.11.11",
        #     "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a": "1646143925",
        #     "__zp_stoken__": "876bdAHxcPSNkZDwsW20PBThzZ31jBix9Mkhdblkob25NEHkVaBppNF8dYBZDTgdHDzt+E0ofMC48VyRAGjkDSjxIdUM0HRhhPx83DyghcARiXDoiNHMgSUAFQ1UtBSsMTQJMZzg/TwV1TSU="
        # }

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
