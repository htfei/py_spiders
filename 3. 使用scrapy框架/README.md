# 说明

## CrawlSpider示例

mytest/crawl_spider_demo.py

目标 抓取所有的名人名言中的[人名,出生日期,出身地点],保存到csv文件中。

### 考虑的问题

- [ ]  一个人有多条名言,但这次抓取只会出现一次，如何过滤？
- [ ]  主界面的列表中没有需要的全部信息，一方面需要找出翻页的url进行跟进，一方面需要找出详情页的url分析数据。

执行 scrapy crawl sp2 -o sp2_2018-04-29.csv

参考 http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spiders.html#crawlspider




