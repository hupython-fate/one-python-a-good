from bs4 import BeautifulSoup
import requests
head={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
fan_hui_ti=requests.get('https://movie.douban.com/explore',headers=head)
print(fan_hui_ti)
print(fan_hui_ti.text)
u=



