# -*- coding: utf-8 -*-
import scrapy
from tupian.items import CourseImageItem
from scrapy.linkextractors import LinkExtractor
from time import sleep
from scrapy.spiders import Rule
class CourseSpider(scrapy.spiders.CrawlSpider):
    name = 'course'
    start_urls = ['http://kmqjh.org/']
    rules=(
    Rule(LinkExtractor(allow="http://kmqjh.org/Item/list.asp\?id=\d*?"),
    callback="parse_course",
    follow = True
    ),
    Rule(LinkExtractor(allow="http://kmqjh.org/Item/Show.asp\?m=1&d=\d.*?"),
    callback="parse_show",
    follow = True
    ),
    )
    def parse_course(self, response):
        item = CourseImageItem()
        getlst=[]
        for tmp_url in response.xpath('//div[@class="content"]//img/@src').extract():
            if tmp_url.find('p://')<1:
               tmp_url='http://kmqjh.org' + tmp_url
            getlst.append(tmp_url)
        item['image_urls'] = getlst
        item['name'] = response.xpath('//head/title/text()').extract_first()
        item['desc'] = response.xpath('//div[@class="content"]//p/text()').extract()
        item['url']=response.url
        yield item
        sleep(2)

    def parse_show(self, response):
        item = CourseImageItem()
        getlst=[]
        for tmp_url in response.xpath('//div[@class="content"]//img/@src').extract():
            if tmp_url.find('p://')<1:
               tmp_url='http://kmqjh.org' + tmp_url
            getlst.append(tmp_url)
        item['image_urls'] = getlst
        item['name'] = response.xpath('//head/title/text()').extract_first()
        item['desc'] = response.xpath('//div[@class="content"]//p/text()|//div[@class="content"]//span/text()').extract()
        item['url']=response.url
        yield item
        sleep(10)

