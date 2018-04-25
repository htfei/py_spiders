# -*- coding: utf-8 -*-
from scrapy.selector import Selector

myhtml = '''
<tr height="19">
<td class="et16" style="BORDER-TOP: #000000 0.5pt solid; FONT-WEIGHT: 400; FONT-SIZE: 10pt; VERTICAL-ALIGN: middle; WIDTH: 320.25pt; COLOR: #000000; FONT-STYLE: normal; WHITE-SPACE: normal; HEIGHT: 14.25pt; TEXT-DECORATION: none; mso-protection: locked visible" width="427" colspan="6" height="19" x:str="">面积单位：平方米</td>
<td class="et19" style="BORDER-TOP: #000000 0.5pt solid; FONT-WEIGHT: 400; FONT-SIZE: 10pt; VERTICAL-ALIGN: middle; WIDTH: 266.25pt; COLOR: #000000; FONT-STYLE: normal; WHITE-SPACE: normal; HEIGHT: 14.25pt; TEXT-ALIGN: center; TEXT-DECORATION: none; mso-protection: locked visible" width="355" colspan="5" height="19" x:str="">统计日期：2018-0<font size="2"><span class="font3">1</span><span class="font3">-</span><span class="font3">31</span><span class="font3"><span style="mso-spacerun: yes">&nbsp;</span>17:00:00<span style="mso-spacerun: yes">&nbsp;</span>至<span style="mso-spacerun: yes">&nbsp;</span>201</span><span class="font3">8</span><span class="font3">-</span><span class="font3">0</span><span class="font3">2</span><span class="font3">-</span><span class="font3">01</span><span class="font3"><span style="mso-spacerun: yes">&nbsp;</span>17:00:00</span></font></td></tr>
'''

myhtml = myhtml.replace(u'&nbsp;', u' ')
#print(myhtml)
a = Selector(text=myhtml).xpath('//tr/td[2]//text()').extract()
print(u"".join(a))

s = '''<td align="center" class="newstitle">2018年2月1日新建商品房成交统计情况</td>'''
s2 = Selector(text=s).xpath('//td[@class="newstitle"]/text()')[0].extract()
print(s2)