from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time


def setup_stealth_driver():
    """配置反检测的浏览器驱动"""
    options = Options()

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

    return driver


# 使用反检测配置
driver = setup_stealth_driver()
try:
    driver.get('https://www.qidian.com/rank/')
    time.sleep(3)  # 等待页面加载

    # 检查是否成功绕过检测
    if "captcha" not in driver.page_source.lower():
        print("成功绕过检测!")
        print(driver.page_source[:1000])  # 打印前1000字符查看
    else:
        print("仍然被检测到，需要更高级的方案")

finally:
    driver.quit()