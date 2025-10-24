import requests
from bs4 import BeautifulSoup

def pa_xin_wen(url):
    response=requests.get(url)
    if response.status_code==200:
        soup=BeautifulSoup(response.content,'html.parser')
        tag_a=soup.select('a')#列表
        for t in tag_a:
            print(t)
    else:
        print(response.status_code)















if __name__ == '__main__':
    url='https://www.qidian.com/'
    pa_xin_wen(url)