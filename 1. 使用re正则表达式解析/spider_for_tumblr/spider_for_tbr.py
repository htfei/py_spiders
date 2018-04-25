__author__ = 'Terry'
# coding=utf8
import requests
import re
import sys
import importlib
importlib.reload(sys)
import codecs

#hea是我们自己构造的一个字典，里面保存了user-agent
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}

# 数据结构字典
file_dict={
    #'author': 'xiaomi',
    #'post_id': 153830201928,
    'file_name': 'aaa',
    'pic_url': 'http://baidu.com/aaa.jpg',
    'video_url': 'http://baidu.com/aaa/xxx',
    'video_type': 'video/mp4'
    #'record_time':'2017-03-04 17:50:42'
}

'''
# 文件内容请求
print('now downloading:' + each)
pic = requests.get(each)
# 文件保存
fp2 = open('output\\' + pic_name.group(), 'wb')
fp2.write(pic.content)
fp2.close()
'''

class Tbr_Spider(object):
    def __init__(self):
        print(u'开始爬取内容...')

    # 获取网页源代码
    def get_page(self,url):
        html = requests.get(url,headers=hea)
        html.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
        print(html.content)
        return html.text

    # 下载图片,视频
    def download_file(self,url,name):
        # 文件内容请求
        print('now downloading:' + url)
        file_buffer = requests.get(url)
        # 文件保存
        fp = open('output\\' + name, 'wb')
        fp.write(file_buffer.content)
        fp.close()
        print('downloading: ' + url + ' ok!')

    # dict记录到info.txt
    def set_dict_to_file(self,file_dict):
        info_fp = open('output\\info.txt', 'a')
        info_fp.writelines(str(file_dict)+'\n')
        info_fp.close()

    # 抓取每个div块的信息
    def get_goal_div(self,src_str):
        div_list = re.findall('(<div class="post_media".*?</video>)',src_str,re.S)
        #print(div_list)
        return div_list


    def set_file_dict(self,src_str):
        pic_url_list = re.findall('<video.*?poster=\'(.*?)\'.*?<source src="(.*?)".*?type="(.*?)"',src_str,re.S)
        #print(pic_url_list)
        for each in pic_url_list:
            #更新字典值
            file_dict['pic_url'] = each[0]
            file_dict['video_url'] = each[1]
            file_dict['video_type'] = each[2]
            file_dict['file_name'] = re.search('(\w+)\.jpg',each[0],re.S).group()
            print(file_dict)

            # dict记录到info.txt
            self.set_dict_to_file(file_dict)

            # 下载图片和视频
            self.download_file(file_dict['pic_url'], file_dict['file_name']+'.jpg')
            #self.download_file(file_dict['video_url'], file_dict['file_name']+'.mp4')


if __name__ == '__main__':

    # 声明一只爬虫
    tbr_spider = Tbr_Spider()

    # 将网页源码加载到一个str字符串
    # page_fp = open('output\\src.htm', 'r+',encoding="utf8")
    # page_str = page_fp.read()
    #print("重新读取字符串 : ", page_str)

    html_url='https://www.tumblr.com/dashboard'
    page_str = tbr_spider.get_page(html_url)

    # 将网页str中需要的div模块提取到一个list列表
    div_list = tbr_spider.get_goal_div(page_str)
    for div_obj in div_list:
        # 从div提取信息到dict
        tbr_spider.set_file_dict(div_obj)
