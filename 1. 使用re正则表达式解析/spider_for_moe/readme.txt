# this spider is made for moe (URL:http://moe.005.tv/)
# 使用方法
# 选中你要采集的网站的URL,若你只有一个




# 采集方案（开发思路）

# 网址规律分析（√）
# 若只有1页，那么URL为http://moe.005.tv/number.html
# 若共有X页，那么X页的URL为http://moe.005.tv/number_X.html

# 分页分析（√）
# 分页块    FENYE_DIV = "(<div class="fenye">.*?</div>)"
# 分页列表  FENYE_LIST_RE = "<a href='(.*?)'"

# 内容块分析
# DIV_LIST_RE = '(<div class="content_nr">.*?<img .*?</div>)'


# 目标资源分析（√）
# 本站目标资源为img, RES_URL_RE = '<img.*?src="(.*?)"'
