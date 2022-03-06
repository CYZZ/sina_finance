# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagedownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # 该方法可以接收爬虫文件提交过来的item对象，
    name = scrapy.Field()
    url = scrapy.Field()
    
    # pass
