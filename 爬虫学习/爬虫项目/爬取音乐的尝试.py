import requests
from bs4 import BeautifulSoup
from selenium.webdriver.edge.options import Options
from selenium import webdriver
import time

def pa_yin_yue(url):
    kai_shi = time.time()
    option=Options()
    option.add_argument("--headless")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    driver=webdriver.Edge(options=option)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    html=driver.page_source#获取经过动态渲然后的源代码。
    soup=BeautifulSoup(html,'html.parser')
    yin_yue_url=[]

    yin_yue_url111=soup.find_all('script')
    for tag in yin_yue_url111:
        url1=tag.get('src')
        if url1:                           #这几行的功能是把源代码中的script标签的src属性的值添加到yin_yue_url这个列表中。
            yin_yue_url.append(url1)

    yin_yue_url222=soup.find_all('a')
    for tag2 in yin_yue_url222:
        url2=tag2.get('href')       #这几行代码的功能是把源代码中的a标签的href属性的值添加到yin_yue_url这个列表中。
        if url2:
            yin_yue_url.append(url2)

    yin_yue_url333=soup.find_all('iframe')
    for tag3 in yin_yue_url333:
        url3=tag3.get('src')        #这几行代码的功能是把源代码中的iframe标签的src属性的值添加到yin_yue_url这个列表中。
        if url3:
             yin_yue_url.append(url3)

    yin_yue_url444=soup.find_all('link')
    for tag4 in yin_yue_url444:
        url4=tag4.get('href')     #把link标签的href属性的值添加到yin_yue_url.
        if url4:
            yin_yue_url.append(url4)


            #加if url:   是为了去除空值。

    you_xiao_url2=[]

    for you_xiao_url in yin_yue_url:
        if you_xiao_url.startswith('//'):
            u2='http:'+you_xiao_url
            you_xiao_url2.append(u2)
        elif you_xiao_url.startswith('/'):
            u2='http://www.52wusun.com'+you_xiao_url
            you_xiao_url2.append(u2)
        elif you_xiao_url.startswith(("https://","http://")):
            you_xiao_url2.append(you_xiao_url)

    print(f"共提取出{len(you_xiao_url2)}个有效的url(资源标识符)。")
    end_time=time.time()
    zhong_time=end_time-kai_shi
    print(f"共耗时{zhong_time}秒。")
    #下一步是设计一个过滤机制，把无效的url变为有效的url.

if __name__ == '__main__':
    url="http://www.52wusun.com/19783.html"
    pa_yin_yue(url)


#print(dir(str))
