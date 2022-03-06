import scrapy

from imgsPro.items import ImgsproItem


class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://sc.chinaz.com/tupian/']

    def parse(self, response):
        div_list = response.xpath('/html/body/div[2]/div[5]/div[1]/div[2]/div/div')
        print(div_list)
        for div in div_list:
            # 注意：使用伪装的属性，防止懒加载的时候无法定位到指定的数据
            src = 'https:' + div.xpath('./div/a/img/@src2').extract_first()
            item = ImgsproItem()
            item['src'] = src
            yield item
            # print(src)


