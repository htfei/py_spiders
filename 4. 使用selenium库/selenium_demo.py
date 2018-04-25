# coding=utf-8
'''
Created on 2018-1-26
@author: htf
Project:使用Chrome浏览器
'''

''' demo1
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('http://www.baidu.com')
driver.find_element_by_id('kw').send_keys('Selenium')
driver.find_element_by_id('su').click()
#driver.quit()
'''

from selenium import webdriver
browser = webdriver.Chrome()
browser.get("http://www.zhihu.com/explore")
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
