from bs4 import BeautifulSoup
import requests
head={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
fan_hui_ti=requests.get('https://movie.douban.com/explore#:~:text=%E5%8D%8E%E8%AF%AD-,%E6%AC%A7%E7%BE%8E,-%E9%9F%A9%E5%9B%BD',headers=head)
print(fan_hui_ti)
print(fan_hui_ti.text)
u=BeautifulSoup(fan_hui_ti.text,"html.parser")#解析和整理函数。
print(u.p)
print(u.a)

ca_zao_zhi_din_nei_rong=u.find_all('div',)
print(ca_zao_zhi_din_nei_rong)

#<span class="drc-subject-info-title-text">凶器</span>
