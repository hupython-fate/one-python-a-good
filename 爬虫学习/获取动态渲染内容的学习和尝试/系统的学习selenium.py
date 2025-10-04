# 安装必要的库
# pip install selenium webdriver-manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# 最简单的启动方式 - 自动下载和管理浏览器驱动
def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

# 测试启动
driver = setup_driver()
driver.get("https://httpbin.org/html")
print("浏览器标题:", driver.title)
driver.quit()