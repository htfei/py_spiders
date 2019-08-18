# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MyCrawlSpider(CrawlSpider):
    '''
    继承自CrawlSpider的demo
    '''
    name = 'gg'
    allowed_domains = ['www.guanggoo.com']
    start_urls = ['http://www.guanggoo.com/?tab=latest']
    rules = (
        # 提取匹配链接并跟进
        Rule(LinkExtractor(allow=('www.guanggoo.com/?tab=latest&p=(\d*)/', ))),

        # 提取匹配链接并分析item
        Rule(LinkExtractor(allow=('quotes.toscrape.com/author/(.*?)', )), callback='parse_item'),
    )

    def parse_item(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self) # shell调试
        for quote in response.xpath('//div[@class="author-details"]'):
            return {
                'author': quote.xpath('.//h3[@class="author-title"]/text()').extract_first(),
                'borndate': quote.xpath('.//span[@class="author-born-date"]/text()').extract_first(),
                'bornloc': quote.xpath('.//span[@class="author-born-location"]/text()').extract_first(),
            }


