# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImagedownloadPipeline:
    fp = None
    # 重写父类的方法，该方法只可以在开始的时候知道用一次
    def open_spider(self, spider):
        print('开始爬虫…………')
        self.fp = open('unused/meinv.txt','w',encoding='utf-8')


    # 专门用来处理item类型对象
    # 该方法可以接收爬虫问价你提交过来的item对象
    # 该方法每接收到一个item，就会被调用一次
    def process_item(self, item, spider):
        name = item['name']
        url = item['url']
        # 进行持久化存储
        self.fp.write(name + '\n' + url + '\n')
    
        #填写return之后，可以在其他次优先级的管道类中收到
        return item
    def close_spider(self, spider):
        print('结束爬虫…………')
        self.fp.close()
