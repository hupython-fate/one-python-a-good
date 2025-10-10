from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
options=Options()
# 反检测配置
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Edge(options=options)
    # 执行JavaScript移除webdriver属性
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
url="https://www.lofter.com/tag/%E8%AF%A1%E7%A7%98%E4%B9%8B%E4%B8%BBoc"
driver.get(url)

phone_input = driver.find_element(By.NAME, "phone")
phone_input.send_keys("你的手机号")

time.sleep(60)
html=driver.page_source
soup=BeautifulSoup(html,'html,parser')
l=soup.find_all('h2')
book_title=[]
for v in l:
    book_title.append(v.string)
f=str(book_title)
with open('./在lofter爬取的诡秘同人文书名.txt','w',encoding='utf-8') as g:
    g.write(f)









