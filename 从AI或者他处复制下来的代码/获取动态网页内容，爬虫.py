from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 设置浏览器选项
options = Options()
options.add_argument('--headless')  # 无界面模式

# 启动浏览器
driver = webdriver.Chrome(options=options)



try:
    driver.get('你的URL')
    time.sleep(3)  # 等待页面加载

    # 获取渲染后的HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 现在可以找到动态加载的内容了
    elements = soup.find_all('span', class_='drc-subject-info-title-text')
    for element in elements:
        print(element.text)
finally:
    driver.quit()