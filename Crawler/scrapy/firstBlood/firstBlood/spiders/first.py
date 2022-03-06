import scrapy


class FirstSpider(scrapy.Spider):
    # 爬虫的文件名称，即使唯一标识
    name = 'first'
    # 允许的域名：用来限定start_urls中列表中哪些url可以进行请求发送
    # allowed_domains = ['www.xxx.com'] # 通常不添加，直接请求所有start的域名吓得数据
    # 起始的url列表：该列表中存放的url会被scrapy自动进行请求和发送
    start_urls = ['https://www.baidu.com/','https://www.sogou.com','https://www.taobao.com']

    # 用于数据解析：response参数表示的就是请求成功后对应的响应对象。
    def parse(self, response):
        print(response)
        # pass
