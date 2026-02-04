from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

def jian_xi_cai_jing(url):
    op=Options()
    op.add_argument("--disable-blink-features=AutomationControlled")
    op.add_experimental_option("excludeSwitches", ["enable-automation"])
    op.add_experimental_option('useAutomationExtension', False)
    op.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    op.add_argument('--headless')
    driver=webdriver.Edge(options=op)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(url)
    time.sleep(5)
    html=driver.page_source
    so=BeautifulSoup(html,'html.parser')
    huo_de=so.find_all('div')
    for x in huo_de:
        if x.string is not None:
            print(x.string)
    driver.quit()

url='https://zsjy.jxufe.edu.cn/listPage?index=9&id=0'
jian_xi_cai_jing(url)

#运行此程序，会自动打印出本年的，江西财经大学的本科招生网的招生简章目录。