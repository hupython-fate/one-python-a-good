from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time


def pa_qu(url):
    global c
    op=Options()
    op.add_argument("--disable-blink-features=AutomationControlled")
    op.add_experimental_option("excludeSwitches", ["enable-automation"])
    op.add_experimental_option('useAutomationExtension', False)
    op.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    dri=webdriver.Edge(options=op)
    dri.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    dri.get(url)
    time.sleep(5)
    html=dri.page_source
    #现在竟然还要手动分析页面结构，才能从中提取出信息，真是不够自动化，要是能使程序自动分析页面结构，那就好了。
    soup=BeautifulSoup(html,'html.parser')
    f=soup.find_all('h4')
    v=1
    for c in f:
        print(f'{v},{c.string}')
        v+=1
    j=c.string
    dri.quit()
    return f


url="https://jxzsb.cn"
#url=input('请输入你想要查询的url:')
shu_ju=pa_qu(url)
ll=str(shu_ju)
with open('./爬取到的2025年的专升本招生院校（35所）.txt','w',encoding='utf-8') as f:
    f.write(ll)

