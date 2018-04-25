# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MyCrawlSpider(CrawlSpider):
    name = 'whhouse'
    allowed_domains = ['scxx.fgj.wuhan.gov.cn']
    start_urls = ['http://scxx.fgj.wuhan.gov.cn/scxxbackstage/whfcj/channels/854.html']
    rules = (
        # 提取匹配链接并跟进
        Rule(LinkExtractor(allow=('http://scxx.fgj.wuhan.gov.cn/scxxbackstage/whfcj/channels/854_(\d*).html'))),

        # 提取匹配链接并分析item
        Rule(LinkExtractor(allow=('http://scxx.fgj.wuhan.gov.cn/scxxbackstage/whfcj/contents/854/(\d*).html', )), callback='parse_item'),
    )


    def parse_item(self, response):
        data = []
        for i,node in enumerate(response.xpath('//*[@id="artibody"]/table/tbody/tr')):
            if i in range(2,18):
                data.append(node.xpath('.//td//text()').extract()) #/text()表示所有td节点的内容
                # TODO 使用xpath表达式对text()进行筛选,排除'\xa0'的内容 or 对response进行编码转化 or 将'\xa0'替换为''
        yield {
            'title': response.xpath('//td[@class="newstitle"]//text()')[0].extract(),
            'data': data
        }

