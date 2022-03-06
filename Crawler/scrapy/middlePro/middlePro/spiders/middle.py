import scrapy


class MiddleSpider(scrapy.Spider):
    # 请求拦截，设置
    name = 'middle'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.baidu.com/s?wd=ip']

    def parse(self, response):
        page_text = response.text
        with open('unused/ip.html','w',encoding='utf-8') as fp:
            fp.write(page_text)
        # pass
