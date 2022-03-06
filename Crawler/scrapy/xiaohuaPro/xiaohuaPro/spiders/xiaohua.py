from urllib.request import Request
import scrapy


class XiaohuaproSpider(scrapy.Spider):
    '''
    本案例是测试全栈的数据请求爬虫
    '''
    name = 'xiaohua'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.netbian.com/meinv/index.htm']
    # http://www.netbian.com/meinv/index_2.htm # 第二页
    # 生成一个通用的模板（不可变）
    url = 'http://www.netbian.com/meinv/index_%d.htm'
    page_num = 2

    def parse(self, response):
        li_list = response.xpath('/html/body/div[2]/div[2]/div[3]/ul/li')
        # print(li_list)
        for li in li_list:
            img_name = li.xpath('./a/b/text()').extract_first()
            print(img_name)
        print('\n\n第',self.page_num)
        # 递归调用
        if self.page_num <= 11:
            new_url = format(self.url%self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=new_url,callback=self.parse)
