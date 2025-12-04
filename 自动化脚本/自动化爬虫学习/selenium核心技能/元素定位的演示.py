from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 启动浏览器
driver = webdriver.Edge()

try:
    # 打开百度
    driver.get("https://www.baidu.com")

    # 方法1：通过ID定位搜索框（最常用）
    search_box = driver.find_element(By.ID, "kw")
    search_box.send_keys("Selenium教程")

    # 方法2：通过ID定位搜索按钮
    search_btn = driver.find_element(By.ID, "su")
    search_btn.click()

    # 等待结果加载
    time.sleep(3)

    # 方法3：通过CLASS_NAME定位第一个搜索结果
    first_result = driver.find_element(By.CLASS_NAME, "c-title-text")
    print(f"第一个结果: {first_result.text}")

    # 点击第一个结果
    first_result.click()

    time.sleep(3)

finally:
    driver.quit()