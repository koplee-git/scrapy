# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from json import loads
from zhiuhuuser.items import UserItem
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_user="qing-rui-qi-ji"
    user_url='https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    fans_follow_url="https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={set}&limit={limit}"
    fans_follow_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    close_follow_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={set}&limit={limit}'
    close_follow_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield Request(self.fans_follow_url.format(user=self.start_user,include=self.fans_follow_query,set=0,limit=20),callback=self.parse_fans)
        yield Request(self.close_follow_url.format(user=self.start_user,include=self.close_follow_query,set=0,limit=20),callback=self.parse_close)
    
    def parse_user(self, response):
        result=loads(response.text)
        items=UserItem()
        for field in items.fields:
            if field in result.keys():
                items[field]=result.get(field)
                yield items

    def parse_fans(self,response):
        result=loads(response.text)
        if "data" in result.keys():
            for num in result.get('data'):
                if "url_token" in num.keys():
                    yield Request(self.user_url.format(user=num.get('url_token'),include=self.user_query),callback=self.parse_user)
        if "paging" in result.keys():
            if not result['paging'].get('is_end'): 
                yield Request(result['paging'].get('next'),callback=self.parse_fans)
    
                
    def parse_close(self,response):
        restul=loads(response.text)
        if "data" in restul.keys():
            for num in restul.get('data'):
                if "url_token" in num.keys():
                    yield Request(self.user_url.format(user=num.get('url_token'),include=self.user_query),callback=self.parse_user)
        if "paging" in restul.keys():
            if not restul['paging'].get('is_end') :
                yield Request(restul['paging'].get('next'),callback=self.parse_close)
