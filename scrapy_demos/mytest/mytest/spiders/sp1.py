# -*- coding: utf-8 -*-
import scrapy


class Sp1Spider(scrapy.Spider):
    name = 'sp1'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(), #绝对子节点
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(), #相对子节点
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract() #匹配多个
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
