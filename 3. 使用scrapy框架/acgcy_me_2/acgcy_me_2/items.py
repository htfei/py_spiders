# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcgcyMe2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    down_url = scrapy.Field()
    down_pwd = scrapy.Field()
    pass
