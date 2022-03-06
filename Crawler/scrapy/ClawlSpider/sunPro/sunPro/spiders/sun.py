import scrapy
# 链接提取器
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/world/']
    # 链接提取器:根据制定规则（allow=“正则”）进行指定链接的提取
    Detaillink = LinkExtractor(allow=r'news/article/H1(.*).html')
    # https://www.163.com/news/article/H1MIJ01V00018AP1.html
    
    rules = (
        # 规则解析器：将链接提取器提取到的链接进行指定规则 (callback)的解析操作
        # Rule(link, callback='parse_item', follow=True),
        Rule(Detaillink, callback='parse_item_detail', follow=False),
        # follow = True：可以将链接提取器继续作用到链接提取到的链接所对应的页面中。
    )

    def parse_item(self, response):
        print("收到了item response")
        print(response)
        return
        # xpath不能包含tbody可以使用/代替，直接跳过上一个标00
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
    def parse_item_detail(self, response):
        print(response)
        title = response.xpath('/html/body/div[3]/div[1]/h1/text()').extract_first()
        new_content = response.xpath('/html/body/div[3]/div[1]/div[3]/div[2]/p[3]/text()').extract_first()
        print('标题：',title)
        print('内容：',new_content)