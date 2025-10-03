import requests
url='https://www.douban.com/'
heade={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}#伪装成浏览器
response=requests.get(url,headers=heade)
print('查看状态码：',response.status_code)#打印状态码，查看是否请求成功。
print('查看响应内容',response.text)


import re

#下一步是解析数据，用re正则表达式

mou_shi=r'电影+'
ddd=re.findall(mou_shi,response.text)
print(ddd)
huo_qu_wan_zhi=r'https?'
ff=re.findall(huo_qu_wan_zhi,response.text)
print(ff)
xin_=r'<a(.*?)>'#非贪婪的匹配 <a 开始标签，然后非贪婪地匹配任意字符，直到遇到 > 结束标签。
#使用了分组（）和通配“.*？”。
kk=re.findall(xin_,response.text)
print(kk)
#可以用差不多的形式把所有的网址提取出来。
wan_zhi=r'http(.*?)"'
wan=re.findall(wan_zhi,response.text)
print(wan)