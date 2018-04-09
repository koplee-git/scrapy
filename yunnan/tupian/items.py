# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 要下载的图片 url 列表
    image_urls = scrapy.Field()
    # 下载的图片会先放着这里
    images = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
