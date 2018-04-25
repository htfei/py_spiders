# coding=utf8
import requests
import re
import sys
import importlib
importlib.reload(sys)

class spider(object):
    def __init__(self):
        print(u'开始爬取内容。。。')

#getsource用来获取网页源代码
    def getsource(self,url):
        html = requests.get(url)
#        print(html.content)
        return html.text

#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

#dowmloadfile下载url对应的目标文件到本地目录,并返回url
    def dowmloadfile(self,eachclass):
        pic_url=re.findall('<img.*?src="(.*?)"',eachclass,re.S)
        i = 0
        for each in pic_url:
            print('now downloading:' + each)
            pic=requests.get(each)
            fp=open('pic\\' + str(i)+'.jpg', 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
            f = open('info.txt', 'a')
            f.writelines('pic_' + str(i) + ':' + each + '\n')
        f.close()



if __name__ == '__main__':
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    jikespider = spider()
    all_links = jikespider.changepage(url,2)
    for link in all_links:
        print(u'正在处理页面：' + link)
        html = jikespider.getsource(link)
        jikespider.dowmloadfile(html)



