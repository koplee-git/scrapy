#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re
 
 
class ZidingyiPipeline(ImagesPipeline):
    
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = request.meta['name']
        headername = request.meta['url'][-4:]
        image_guid =headername + "--"+request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder,image_guid)
        return filename  
 
    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        for i,img_url in enumerate(item['image_urls']):
            url = item['url']
            name  = item['name']
            yield Request(img_url, meta={'item': item,
                                         'url': url,
                                         'name': name})
 
 
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
 
    # def process_item(self, item, spider):
    #     return item
 

class WritePipeline(object):
    def process_item(self,item,spider):
        num = item['url'][-4:]
        addr = '/root/scrapy/yunnan/tupian/spiders/images/full/{0}/{1}.txt'.format(item['name'],num)
        with open(addr,'w') as f:
            f.write(str(item['desc']))  
        return item
