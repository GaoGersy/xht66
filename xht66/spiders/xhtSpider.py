# coding:utf-8
import requests
import logging

import scrapy
from scrapy.spiders import CrawlSpider
from xht66.items import Xht66Item


class Spider(CrawlSpider):
    name = 'xhtSpider'
    url = 'http://xht66.com/detail/'
    offset = 500
    singleOffset = 1
    start_urls = [url + str(offset) + ".html"]

    def parse(self, response):
        xpath = list(response.xpath("//p[@class='sx']"))
        for each in xpath:
            # 初始化模型对象
            item = Xht66Item()
            item['link'] = each.xpath("./img/@src").extract()[0]
            item['name'] = each.xpath("./img/@alt").extract()[0]
            yield item

        print(len(xpath))
        print(xpath)
        if len(xpath)==0:
            if self.offset < 5000:
                self.offset += 1
                self.singleOffset=1
            yield scrapy.Request(self.url + str(self.offset) + ".html", callback=self.parse)
        else:
            self.singleOffset += 1
            yield scrapy.Request(
                self.url + str(self.offset) + "_" + str(self.singleOffset) + ".html",
                callback=self.parse)

            # 每次处理完一页的数据之后，重新发送下一页页面请求
            # self.offset自增10，同时拼接为新的url，并调用回调函数self.parse处理Response
            # yield scrapy.Request(self.url + str(self.offset) + ".html", callback=self.parse)
