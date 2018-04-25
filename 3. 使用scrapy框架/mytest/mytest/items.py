# -*- coding: utf-8 -*-
'''
aaa
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MytestItem(scrapy.Item):
    '''
    aaa
    '''
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    borndate = scrapy.Field()
    bornloc = scrapy.Field()
