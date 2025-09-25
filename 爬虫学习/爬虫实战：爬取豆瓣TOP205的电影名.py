from bs4 import BeautifulSoup
import requests
head={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
fan_hui_ti=requests.get('https://movie.douban.com/chart',headers=head)
print(fan_hui_ti)
print(fan_hui_ti.text)
with open('./储存获取的html的源代码.html','w',encoding='utf-8') as k:
    k.write(fan_hui_ti.text)
u=BeautifulSoup(fan_hui_ti.text,"html.parser")#解析和整理函数。
#print(u.p)
#print(u.a)

ca_zao_zhi_din_nei_rong=u.find_all('a')
#print(ca_zao_zhi_din_nei_rong)
for cc in ca_zao_zhi_din_nei_rong:
    print(cc.string)

#<span class="drc-subject-info-title-text">凶器</span>
#我很疑惑，为什么再网页上有的表签和被标签包裹的文字内容，在对这个网页进行爬取后，返回的html源代码中没有呢?

#我有两个猜测，
#一是反爬机制。
#二是我输入的url有问题，不准确。
