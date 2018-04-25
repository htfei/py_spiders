__author__ = 'Terry'
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
#from urllib.parse import urljoin
import io
import sys
import importlib
importlib.reload(sys)
import re

html = '<span style="font-family: arial, helvetica, sans-serif;"> \
<a href="https://pan.baidu.com/s/1skNEw13">ACGCY.ME</a>  密码: iiua  </span>'
#print(re.findall(r"密码: (.+?) ",html))

soup  = BeautifulSoup(html,"lxml")
soup.prettify()
#print(type(soup))

'''
tag = soup.a
print(type(tag))
print(tag)
down_url = soup.select('a')[0]['href']
print(type(down_url))
print(down_url)
'''

tag = soup.text
print(type(tag))
print(tag)
down_pwd = re.findall(r"密码: (.+?) ",soup.text)
print(type(down_pwd))
print(down_pwd)
