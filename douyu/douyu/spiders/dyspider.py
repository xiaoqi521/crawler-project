# -*- coding: utf-8 -*-
import scrapy
from douyu.items import DouyuItem
import json

class DyspiderSpider(scrapy.Spider):
    name = 'dyspider'
    allowed_domains = ['capi.douyucdn.cn']
    offset = 0
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 把json格式的数据转换为Python格式,data段是列表
        data = json.loads(response.text)['data']
        for each in data:
            item = DouyuItem()
            item['nickname'] = each['nickname']
            item['imagelink'] = each['vertical_src']
            item['anchorcity'] = each['anchor_city']

            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback = self.parse)