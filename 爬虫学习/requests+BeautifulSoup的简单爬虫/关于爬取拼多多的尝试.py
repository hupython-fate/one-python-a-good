import requests
from bs4 import BeautifulSoup
#导入第三个库，用于模拟浏览器的加载动态网页内容。
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#import time

key=input('你想要查询的商品：')
head={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
url=f'https://mobile.pinduoduo.com/search_result.html?search_key={key}'
fan_hui_de_hui_yin=requests.get(url,headers=head)
print(fan_hui_de_hui_yin)#状态行
html=fan_hui_de_hui_yin.text#响应体
#print(html)

jie_xi_html=BeautifulSoup(html,'html.parser')#解析后的响应体。
print(jie_xi_html)



#总结，html源代码爬是爬出来了，但是不能获取动态的网页html源代码，
# 也就不能爬到我想要的信息，对使用javaScrpt进行实时渲染的一些网战，根本就毫无用处，但对某些网站，比如说诗词网，甚至不用伪装浏览器。