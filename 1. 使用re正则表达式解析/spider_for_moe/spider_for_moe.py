# coding=utf8
import requests
import re
import io
import os
import sys
import importlib
importlib.reload(sys)

# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

# todo: [优化]保存目录按标题创建
# todo: [升级]配置信息写入ini文件
# todo: [升级]生成exe可执行文件
# todo: [bug]分析打印函数延时的原因，（猜测和未刷新flush缓冲区有关）
# todo: [bug]分析atom编译环境下找不到目录文件的错误原因，PS:pycharm下编译正常（猜测atom环境的bug）
# 适用范围：一组图片分成多个网页显示，一页只有几张图片的网站

# 初始网页URL,网页URL规律（一个正则表达式str）
FIRST_PAGE_URL = 'http://moe.005.tv/70010.html'  # 不通用
HOST_URL = 'http://moe.005.tv/'
RES_SAVE_PATH_RE = '(\d+).html'     # 获取60474

# 网页URL组 （分析URL规则得到,默认网页数量10页）
PAGE_LIST_RE = '51323_(\d+).html'  # 不通用
PAGE_LIST_RE_STR = '51323_%s.html'  # 不通用
PAGE_LIST_COUNTS = 4           # 设置为1，表示只有一页


# 分页分析（√）
# 分页块
FENYE_DIV_RE = '(<div class="fenye">.*?</div>)'
# 分页列表
FENYE_LIST_RE = "<a href='(.*?)'"


# div组 获取规则
DIV_LIST_RE = '(<div class="content_nr">.*?<img .*?</div>)'  # 不通用
# todo: [bug]当<img/>块之间存在<div/>时，将会导致子<div>之后的<img>匹配不到(目前还没看到此类网页)

# 资源url提取规律 （一个正则表达式str）,资源名称,储存位置，日志记录文件
RES_URL_RE = '<img.*?src="(.*?)"'
RES_NAME_RE = '(\w+\.(jpg|jpeg|png|gif))'
RES_SAVE_PATH = 'nowdir'     # 自定义，小心覆盖之前的
RES_URL_FILE = 'info.txt'   # 自定义，小心覆盖之前的


# 网页标题 获取规则
HTML_TITLE_RE = '<title>(.*?)</title>'

class Spider(object):

    def __init__(self):
        print(u'now start spider...')

    # 生产不同页数的链接
    @staticmethod
    def set_page_url_list(url, url_counts):
        page_list = []
        if url_counts > 1:
            now_page = int(re.search(PAGE_LIST_RE, url, re.S).group(1))
            for i in range(now_page, url_counts+1):
                now_link = re.sub(PAGE_LIST_RE, PAGE_LIST_RE_STR %i, url, re.S)
                page_list.append(now_link)
        else:
            page_list.append(url)
        print('page_list:', page_list)
        return page_list

    # 提取目标div（单个）
    @staticmethod
    def get_goal_div2(goal_div_re, src_str):
        print(u'get_goal_div2...')
        goal_div = re.search(goal_div_re, src_str, re.S)
        if goal_div:
            print(u'goal_div:', goal_div.group(1))  # div_list中含有中文会导致print异常
            return goal_div.group(1)
        else:
            print(u'not found goal_div.')
            return 'none'


    # 获取网页源代码
    @staticmethod
    def get_page_html(page_url):
        print(u'get_page_html:' + page_url)
        page_html = requests.get(page_url)
        # print(page_html.content)
        # print(html.text)
        return page_html.text

    # 提取网页标题
    @staticmethod
    def get_html_title(html_str):
        print(u'get_page_title...')
        html_title = re.search(HTML_TITLE_RE, html_str, re.S).group(1)
        print('title:' + html_title)
        return html_title

    # 提取目标div列表
    @staticmethod
    def get_goal_div(goal_div_re, src_str):
        print(u'get_goal_div...')
        div_list = re.findall(goal_div_re, src_str, re.S)
        # print(u'div_list:', div_list)  # div_list中含有中文会导致print异常
        return div_list

    # 提取资源url
    @staticmethod
    def get_goal_res(goal_res_re, div_str):
        print(u'get_goal_res...')
        res_list = re.findall(goal_res_re, div_str, re.S)
        print(u'res_list:', res_list)
        return res_list

    # 下载url对应的目标文件
    @staticmethod
    def download_resouces(save_path, res_str):
        print('now downloading res:' + res_str)
        pic = requests.get(res_str)
        pic_name = re.search(RES_NAME_RE, res_str, re.S).group(1)
        fp = open(save_path + '/' + pic_name, 'wb')
        fp.write(pic.content)
        fp.close()
        return True

    # 写入info.txt生成日志文件
    @staticmethod
    def write_log(save_path, log_format, log_text):
        f = open(save_path + '/' + RES_URL_FILE, 'a')  # 以追加模式打开 (从 EOF 开始, 必要时创建新文件)
        f.writelines(log_format + log_text + '\n')
        f.close()
        return True

    # 直接从当前页提取所有的兄弟页面URL
    def get_page_url_list(self, url):
        # 获取page内容
        html = self.get_page_html(FIRST_PAGE_URL)
        # 获取分页div
        fenye_div = self.get_goal_div2(FENYE_DIV_RE, html)
        if fenye_div == 'none':
            print(u'this page not have fenye_div.')
            sys.exit(1)
        # 提取fenye_url
        fenye_list = self.get_goal_res(FENYE_LIST_RE, fenye_div)
        if len(fenye_list) == 0:
            print(u'this page not have fenye.')
            return [FIRST_PAGE_URL]
        # 对fenye_url列表做一次过滤处理
        # 为啥需要过滤？如下分别为[上一页，当前页，第2页，第3页，下一页]
        #（res_list: ['#', '#', '60479_2.html', '60479_3.html', '60479_2.html']）
        # 所以需要去掉上一页和下一页（首尾），并把当前页（#）替换为初始页(FIRST_PAGE_URL)
        url_list = fenye_list[0:len(fenye_list)-1]   # 去掉0和最后一项
        print(u'url_list:', url_list)
        # 对所有的url加上前缀
        for i,j in enumerate(url_list):
            url_list[i] = HOST_URL + j
        print(u'url_list2:', url_list)
        # list.index(obj)从列表中找出某个值第一个匹配项的索引位置
        # url_list[url_list.index(HOST_URL + '#')] = FIRST_PAGE_URL   # # 项替换 ,2018.04.25更新，网站更新了，第一页没有链接了。
        print(u'url_list:', url_list)
        return url_list

if __name__ == '__main__':

    moe_spider = Spider()

    page_flag = 0

    # 手动设置分页URL.
    # all_links = moe_spider.set_page_url_list(FIRST_PAGE_URL, PAGE_LIST_COUNTS)
    # 自动分析分页URL.
    all_links = moe_spider.get_page_url_list(FIRST_PAGE_URL)
    for link in all_links:
        # 获取page内容
        html = moe_spider.get_page_html(link)

        if page_flag == 0:
            # 提取网页标题
            # title = moe_spider.get_html_title(html)
            # title_text = moe_spider.get_html_title(html)
            title = re.search(RES_SAVE_PATH_RE, FIRST_PAGE_URL, re.S).group(1)
            print(u'title:', title)
            # title = RES_SAVE_PATH
            os.mkdir(title)
            moe_spider.write_log(title, 'net_url:', FIRST_PAGE_URL)
            # moe_spider.write_log(title, 'net_title:', title_text)
            page_flag = 1

        # 提取div
        div_list = moe_spider.get_goal_div(DIV_LIST_RE, html)
        for div in div_list:
            # 提取res
            res_list = moe_spider.get_goal_res(RES_URL_RE, div)
            i = 1
            for res in res_list:
                # res_url写入info.txt
                moe_spider.write_log(title, 'res_' + str(i) + ':', res)
                i += 1
                # 下载资源文件
                moe_spider.download_resouces(title, res)
