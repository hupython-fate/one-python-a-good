import requests
from bs4 import BeautifulSoup
def shen_mi():
    book=[]
    for x in range(1,34):
        url = f"https://m.xddxsw.net/883/883862_{x}/index.html"
        head = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
        reso=requests.get(url,headers=head)
        html=reso.text
        soup=BeautifulSoup(html,'html.parser')
        book_name=soup.find_all('li')
        book.append(book_name)
    book_1=str(book)
#with open('./《神秘复苏》的章节名和每一章的http地址.txt','w',encoding='utf-8') as l:
   # l.write(book_1)
#目的是什么？
#通过获取到的每一章的http地址，下载每一章。并保证自动化完成。
    import re
    mou_shi=r'href="(.*?)"'
    book_url=re.findall(mou_shi,book_1)
#with open('./《神秘复苏》每一章的不完整的url.txt','w',encoding='utf-8') as k:
 #   k.write(f_url)
    book_nei_rong=[]
    yy=1
    for x in book_url:
        url='https://m.xddxsw.net'+str(x)
        head = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
        reso=requests.get(url,headers=head)
        html=reso.text
        soup=BeautifulSoup(html,'html.parser')
        fff=soup.find_all('p')
        book_nei_rong.append(fff)
        print(f'第{yy}次循环。')
        yy+=1
    print(book_nei_rong)
shen_mi()
#效果不理想。
'''未完成，效率太低了，可以考虑用aiohttp库，把这个改成并发或异步爬虫。'''






