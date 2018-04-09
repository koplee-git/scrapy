# -*- coding: utf-8 -*-
import scrapy
from tupian.items import CourseImageItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
class CourseSpider(scrapy.spiders.CrawlSpider):
    name = 'course'
    start_urls = ['https://www.shiyanlou.com/courses/']
    rules=(
    Rule(LinkExtractor(allow="https://www.shiyanlou.com/courses/\?category=all&course_type=all&fee=all&tag=all&page=.*?"),
    callback="parse_course",
    follow = True
    ),
    )
    def parse_course(self, response):
        item = CourseImageItem()
        item['image_urls'] = response.xpath('//div[@class="course-img"]/img/@src').extract()
        item['name'] = response.xpath('//div[@class="course-name"]/text()').extract()
        item['desc'] = response.xpath('//div[@class="course-desc"]/text()').extract()
        item['url']=response.url
        yield item


