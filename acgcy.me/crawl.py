#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
import time
import re

url = 'https://acgcy.me/page/{page}/'

#已完成的 页数序号，初始为0
page = 28

nowtime = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
filename = "free_list_"+nowtime+".csv"
csv_file = open(filename,"w",newline='')
csv_writer = csv.writer(csv_file,delimiter=',')

#去掉所有的html标签
reg1 = re.compile("<[^>]*>")
reg2 = re.compile('</?w+[^>]*>')

print('I am beginning ...')
#csv_writer.writerow(["page","标题","url","资源链接","资源提取码"])

while True:
    page += 1
    print('fetch:',url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text,"lxml")
    html.prettify()
    #print(html)

    my_list = html.select('li.post.box.row.fixed-hight')
    #print(len(my_list))
    # 循环在读不到新的房源时结束
    if not my_list:
        print('have no more list , I will exit... ')
        break

    for my_node in my_list:
        node_title = str(my_node.select('.article h2 a')[0]['title'])
        my_node_url = urljoin(url,my_node.select('a')[0]['href'])
        print(node_title)
        if '【VIP】' not in node_title :
            print(node_title)
            csv_writer.writerow([node_title,my_node_url])
            # TODO 解决登录问题 --cookie解决，2018-1-24
            # TODO 解决密码字符串提取问题
            '''
            raw_cookies = 'wordpress_test_cookie=WP+Cookie+check;wordpress_logged_in_cfd21a21547805e125a24a8399e3d16a=why2fly%7C1516897255%7C003GFcYBspDOi3cxs1hlK97TzMk71y1hTHUqK4bsVED%7Cab67459c977526651c036fd7b34e8d51c2c8d8d11ad5506f2b45465d4518f8a4'
            my_cookies={}
            for line in raw_cookies.split(';'):
                key,value=line.split('=',1)#1代表只分一次，得到两个数据
                my_cookies[key]=value

            rsp = requests.get(my_node_url,cookies=my_cookies)
            html2 = BeautifulSoup(rsp.text,"lxml")
            html2.prettify()
            down_node = html2.select('div#post_content > p > strong > span')[0]
            #print(down_node)
            down_url = down_node.select('a')[0]['href']
            print(down_url)
            #down_pwd = down_node.select(':not(a)')[0]
            #print(down_pwd)
            down_pwd = re.findall(r"密码: (.+?) ",''.join(down_node))
            print(down_url+":"+down_pwd)
            csv_writer.writerow([page,node_title,my_node_url,down_url,down_pwd])
            #'''


    if page % 20 == 0:
        print('I have fetch 30 times ,and I will sleep 3s ... ')
        time.sleep(3)

csv_file.close()

print('this is end !')
