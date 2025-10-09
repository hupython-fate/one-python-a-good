from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

options=Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver=webdriver.Edge(options=options)
u_url='https://jsj.jxatei.net/index.php?s=news&c=show&id='
kkk=[]
for c in range(6,19):
    url=u_url+str(c)
    driver.get(url)
    time.sleep(3)
    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    f=soup.find_all('font')
fff=str(kkk)
print(fff)