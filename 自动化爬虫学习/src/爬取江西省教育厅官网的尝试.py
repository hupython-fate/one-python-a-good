import requests
from bs4 import BeautifulSoup
def jyt(url):
    k={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
    resp=requests.get(url,headers=k)
    print(f'现在正在请求中，请求的状态码是：{resp.status_code}')
    if resp.status_code==200:
        soup=BeautifulSoup(resp.text,'html.parser')