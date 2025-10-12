from selenium import webdriver
from selenium.webdriver.edge.options import Options
#from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
def nan_ping():
    options = Options()
    # 反检测配置
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    url='https://www.qidian.com/rank/'
    driver=webdriver.Edge(options=options)
# 执行JavaScript移除webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    time.sleep(8)
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    nei_rong=soup.find_all('h2')#寻找html内的所有h2的标签内容。
    seen_titles = set()  # 创建空集合来记录已见的书名
    y=1
    for v in nei_rong:
        book_title = v.get_text().strip()  # 获取标签内的文本内容
    # 检查是否重复
        if book_title not in seen_titles:
            seen_titles.add(book_title)  # 添加到已见集合
            print(f'书名：{y}, {book_title}')
            y += 1
    fff=str(seen_titles)
    with open('./2025年10月起点男频高排名书籍.txt','w',encoding='utf-8') as f:
        f.write(fff)
nan_ping()
'''以后可以每个月运行一下这个程序，只需点一下，就可以自动获取当月的起点男频排行榜，可以说是一劳永逸了。'''