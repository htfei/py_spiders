#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
#from requests.adapters import HTTPAdapter
#from requests.exceptions import ConnectTimeout,ReadTimeout,HTTPError,RequestException
import csv
import time
import re
import socket
socket.setdefaulttimeout(6)

url = 'https://acgcy.me/page/{page}/'

#nowtime = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
#filename = "free_list_"+nowtime+".csv"
filename = "free_list_20180124_221657.csv"
#已完成的 页数序号，初始为0
page = 30

#csv_file = open(filename,"w",newline='')
#csv_writer = csv.writer(csv_file,delimiter=',')
#csv_writer.writerow(["page","标题","url","资源链接","资源提取码"])

# 会话对象让你能够跨请求保持某些参数,例如cookie , 底层的 TCP 连接将会被重用，从而带来显著的性能提升
s = requests.Session()
raw_cookies = 'wordpress_test_cookie=WP+Cookie+check;wordpress_logged_in_cfd21a21547805e125a24a8399e3d16a=why2fly%7C1516897255%7C003GFcYBspDOi3cxs1hlK97TzMk71y1hTHUqK4bsVED%7Cab67459c977526651c036fd7b34e8d51c2c8d8d11ad5506f2b45465d4518f8a4'
my_cookies={}
for line in raw_cookies.split(';'):
    key,value=line.split('=',1)#1代表只分一次，得到两个数据
    my_cookies[key]=value
requests.utils.add_dict_to_cookiejar(s.cookies,my_cookies)

myheader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}

#配置超时及重试次数
#s.mount('http://', HTTPAdapter(max_retries=3))
#s.mount('https://', HTTPAdapter(max_retries=3))

print('I am beginning ...')

while True:
    page += 1
    print('fetch:',url.format(page=page))
    csv_file = open(filename,"a",newline='')
    csv_writer = csv.writer(csv_file,delimiter=',')

    try:
        response = requests.get(url.format(page=page),headers = myheader,timeout=5)
        #print(response.status_code)
    except requests.exceptions: # TODO
    #except ConnectTimeout or ReadTimeout or HTTPError or RequestException:
        print("something is wrong! =====")
        continue;

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
        #print(node_title)
        if '【VIP】' not in node_title :
            print(node_title)
            #csv_writer.writerow([node_title,my_node_url])
            # TODO 解决登录问题 --cookie解决，2018-1-24
            # TODO 解决密码字符串提取问题 ---tag.text 解决,2018.01.24
            #rsp = s.get(my_node_url) #此处使用session故不需要每次都指定cookie了 #requests.get(my_node_url,cookies=my_cookies)
            try:
                rsp = s.get(my_node_url,headers = myheader,timeout=5)
                #print(rsp.status_code)
            except requests.exceptions:
            #except ConnectTimeout or ReadTimeout or HTTPError or RequestException:
                print("something is wrong! =====")
                continue;

            #rsp.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
            rt = rsp.text.replace(u'\xa0', u' ')  #  解决'gbk' codec can't encode character '\xa0'
            html2 = BeautifulSoup(rt,"lxml")
            html2.prettify()
            down_url_node = html2.select('div#post_content > p > strong > span > a')
            if not down_url_node :
                continue;
            down_url = down_url_node[0]['href']
            #print(down_url)
            soup = html2.select('div#post_content > p > strong > span')
            if not soup :
                continue;
            down_node = soup[0]
            #print(down_node)
            #down_pwd = re.findall(r"密码: (.+?) ",down_node.text) # TODO :无法匹配‘密码:aaaa’ ---
            str1 = down_node.text
            c = str1.find(':') + 1 #获取‘:’后面的str
            str2 = str1[c:]
            down_pwd = str2.strip()
            row = [page,node_title,my_node_url,down_url,down_pwd]
            #print(row)
            csv_writer.writerow(row)

    csv_file.close()

    if page % 20 == 0:
        print('I have fetch 30 times ,and I will sleep 3s ... ')
        time.sleep(3)

csv_file.close()

print('this is end !')
