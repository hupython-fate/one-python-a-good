from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import re
import time
from bs4 import BeautifulSoup
def pa_fan_que():
    options=Options()
# 反检测配置
    options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver=webdriver.Edge(options=options)
    kk_URL='https://fanqienovel.com/library/all/page_'
    b=1
    for x in range(1,100):
        url=kk_URL+str(x)
        driver.get(url)
        time.sleep(3)
        y=driver.page_source
        mou_shi=r'H">(.*?)</'
        f=re.findall(mou_shi,y)
        for c in f:
            print(f'{b},{c}')
            b=b+1
    driver.quit()
pa_fan_que()
'''嗯，分页爬取是没有问题的，因为确实自动爬取到了不同分页的内容，所以值得高兴。
但是爬取的信息并不完整，因为番茄中文网用了一种名为“字体加密”的反爬手段。'''