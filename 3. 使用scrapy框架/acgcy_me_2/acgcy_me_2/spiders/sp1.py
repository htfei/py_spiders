# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
import urllib.request
from acgcy_me_2.items import AcgcyMe2Item

class Sp1Spider(scrapy.Spider):
    name = 'sp1'
    allowed_domains = ['acgcy.me']
    #start_urls = [url]
    url = 'https://acgcy.me/page/{page}/'
    page = 0

    def start_requests(self):
        data={'log':'why2fly@aliyun.com',
            'pwd':'1qaz@WSX',
            'rememberme':'forever',
            'wp-submit':u'登录',
            'redirect_to':'https://acgcy.me/wp-admin/',
            'testcookie':'1'
        }
        url = 'https://acgcy.me/wp-login.php'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(url,formdata = data,callback = self.parse)


    def parseNode(self, response):
        c = response.selector.css('div#post_content > p > strong > span > a::attr(href)')
        d = response.selector.css('div#post_content > p > strong > span::text')
        if c and d :
            #获取云盘链接和提取码
            down_url = c[0].extract().replace(u'\xa0', u' ')
            str1 = d[0].extract().replace(u'\xa0', u' ')
            #print(down_url + ":" + str1)
            if '密码:' in str1 :
                i = str1.find('密码:') + 3
                down_pwd = str1[i:].strip()
                #print(down_url + ":" + down_pwd)
                #保存
                item = response.meta['item'] #读取入参item
                item['down_url'] = down_url
                item['down_pwd'] = down_pwd
                return item

    def parse(self, response):
        nodelist = response.selector.css('li.post.box.row.fixed-hight')
        for selobj in nodelist:
            a = selobj.css('div.article > h2 > a::text')
            b = selobj.css('div.article > h2 > a::attr(href)')
            if a and b :
                nowpage = self.page
                tilte = a[0].extract()
                url = b[0].extract()
                if u'【VIP】' in tilte :
                    print(tilte)
                else :
                    # 访问资源页详细
                    print(tilte + ":" +url)
                    item = AcgcyMe2Item()
                    item['page'] = nowpage
                    item['title'] = tilte
                    item['url'] = url
                    yield scrapy.Request(url,meta={'item':item}, callback=self.parseNode)
        # 下一页
        self.page += 1
        url = self.url.format(page=self.page)
        print('=============fetch:',url)
        yield scrapy.Request(url, callback=self.parse)
