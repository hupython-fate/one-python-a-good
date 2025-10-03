import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

url='https://quotes.toscrape.com/'

resp=requests.get(url,headers=headers)
print(resp.status_code)

xian=resp.text
soup=BeautifulSoup(xian,'html.parser')#把得到的响应体整理成结构化的内容。
ca=soup.find_all('span',class_="text")
#print(ca)
#print(xian)
for xy in ca:
    print(xy.string)


#虽然是一个简单的爬虫，不涉及处理动态内容，也没有很多的反爬机制，但还是令人喜悦的。