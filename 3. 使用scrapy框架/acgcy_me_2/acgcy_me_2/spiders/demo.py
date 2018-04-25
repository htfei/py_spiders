
# -*- coding: utf-8 -*-


'''
url = 'https://acgcy.me/page/{page}/'
page = 1
url.format(page=page)
print(url)
url = url.format(page=page)
print(url)
'''

#import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

str1 = '<div class="article"><h2>\
<a href="https://aaa.com" title="11111">aaaaa</a>\
<a href="https://bbb.com" title="22222">bbbbb</a>\
</h2></div>'

#sel_obj = Selector(text=str1).css('div.article > h2 > a::text')
#sel_obj = Selector(text=str1).xpath('//div/h2/a/text()')
#sel_obj = Selector(text=str1).xpath('//div/h2/a/@href')
sel_obj = Selector(text=str1).css('div.article > h3 > a::attr(href)')
print(sel_obj)
#print(a?sel_obj[0]:'aaaa')
#print(sel_obj[0].extract())
print(sel_obj.extract())
#print(sel_obj.extract()[0])

print(len(sel_obj))

if len(sel_obj) and 1:
    print(sel_obj[0])
