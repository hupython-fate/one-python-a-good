from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
def pa_title(url):
    options=Options()
    options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Edge(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    time.sleep(5)
    #html=driver.page_source#如果用selenium全流程的话，那就不需要这一步。
    #tag=driver.find_elements(By.TAG_NAME,'a')
    #soup=BeautifulSoup(html,'html.parser')
    #tag=soup.find_all('h3',class_="book-info-title")#从原始数据中获得的待二次提取的数据
    #tag_a=soup.find_all('a',target_="_blank")
    tag_a=driver.find_elements(By.CSS_SELECTOR,'a[title]')
    title=[]
    for x in tag_a:
        if x.text:
            title.append(x.text)
    return title
def pa_ye_shu(k):#k为要爬取的页数。
    g_url="https://www.qidian.com/so/%E8%AF%A1%E7%A7%98%E4%B9%8B%E4%B8%BB.html"
    title_list=[]
    i=1
    for ci in range(1,k):
        url=g_url+f'?page={ci}'
        h=pa_title(url)#返回的是列表。
        title_list.append(h)
        print(i)
        i+=1
    l=set(title_list)
    tle=str(l)#变成字符串形式的列表。
    with open("./爬取诡秘之主同人文书名.txt",'w',encoding='utf-8') as f:
        f.write(tle)
def pa():
    kk=int(input("请输入你要爬取的页数："))
    print("请耐心等待结果，要爬的页数越多，爬的时间越久！")
    pa_ye_shu(kk)
pa()


