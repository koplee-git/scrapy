# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem

class GithubspiderSpider(scrapy.Spider):
    name = 'githubspider'
    @property
    def start_urls(self):
        url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
        return(url_tmpl.format(i) for i in range(1,5))

    def parse(self,response):
        i = 0
        print(response)
        for course in response.css('li.col-12.d-block.width-full.py-4.border-bottom.public'):
            item = ShiyanlouItem({
                    'name':course.css('div[class="d-inline-block mb-1"] h3 a::text').re_first('\s*(\w+)'),
                    'update_time':course.css('div[class="f6 text-gray mt-2"] ::attr(datetime)').extract_first()
                    })
            github_url = 'https://github.com/'+response.xpath('//h3/a/@href').extract()[i]
            i +=1
            request = scrapy.Request(github_url,callback=self.parse_more)
            request.meta['item'] = item
            yield request
    def parse_more(self,response):
        item = response.meta['item']
        itemlst = response.xpath('//span[@class="num text-emphasized"]/text()').re('\s+(\d)+')
        item['commits'] = itemlst[0]
        item['branches'] = itemlst[1]
        item['releases'] = itemlst[2]
        return item
