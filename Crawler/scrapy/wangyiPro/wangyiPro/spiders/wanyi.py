from mimetypes import init
import scrapy

from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.edge.options import Options

class WanyiSpider(scrapy.Spider):
    name = 'wanyi'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    #实例化一个浏览器对象
    def __init__(self):
        self.bro = WebDriver(executable_path='./unused/edgedriver_mac64/msedgedriver')


    models_url = [] 
    # 解析五大板块的呢日用
    def parse(self, response):
        # li_list = response.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        li_list = response.xpath('/html/body/div[@class="index2016_wrap"]/div[@class="festival_main"]/div[@class="index2016_content"]/div[@class="index_head"]/div[@class="bd"]/div/ul/li')
        # print(li_list)
        # return
        for index in range(1,6):
            model_url = li_list[index].xpath('./a/@href').extract_first()
            self.models_url.append(model_url)
        
        # 依次对每一个板块进行请求
        for url in self.models_url:
            yield scrapy.Request(url, callback=self.parse_model)

    # 每一个板块对应的新闻标题和内容都是动态加载出来的
    def parse_model(self,response):
        print(response)
        # response.xpath
        # pass
    def close(self, spider):
        self.bro.quit()