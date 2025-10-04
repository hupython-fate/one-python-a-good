from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

options=Options()
# 反检测配置
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver=webdriver.Edge(options=options)
kk_URL='https://fanqienovel.com/library/all/page_'
for x in range(1,100):
    url=kk_URL+str(x)
    driver.get(url)
    time.sleep(30)
    y=driver.page_source

