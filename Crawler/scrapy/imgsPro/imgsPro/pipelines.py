# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class ImgsproPipeline:
#     def process_item(self, item, spider):
#         return item

from scrapy.pipelines.images import ImagesPipeline
import scrapy
# 管道类封装
class ImgsPileLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['src'])
        # return super().get_media_requests(item, info)

    # 指定图片的存储路径
    def file_path(self, request, response=None, info=None, *, item=None):
        imgName = request.url.split('/')[-1]
        return imgName
        # return super().file_path(request, response, info, item=item)

    def item_completed(self, results, item, info):
        print("开始返回item")
        return item
        # return super().item_completed(results, item, info)
