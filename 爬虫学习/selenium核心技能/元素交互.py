from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver=webdriver.Edge()
url='https://www.douban.com/'
driver.get(url)
time.sleep(20)


# 输入框操作
text_input = driver.find_element(By.ID, "user-message")
text_input.clear()       # 清空现有文本
text_input.send_keys("你好，世界！") # 输入文本

# 点击操作
button = driver.find_element(By.ID, "show-message")
button.click()

# 下拉列表操作 - 需要使用Select类
from selenium.webdriver.support.ui import Select
dropdown = Select(driver.find_element(By.ID, "cars"))
dropdown.select_by_visible_text("奥迪")   # 根据显示文本选择
dropdown.select_by_value("audi")          # 根据value属性选择
dropdown.select_by_index(2)               # 根据索引选择 (从0开始)

# 单选按钮和复选框
checkbox = driver.find_element(By.ID, "agree-terms")
if not checkbox.is_selected():
    checkbox.click() # 如果没被选中，则点击

radio_button = driver.find_element(By.ID, "gender-male")
radio_button.click()

# 获取元素信息
element = driver.find_element(By.ID, "some-element")
print(f"元素文本: {element.text}")
print(f"元素属性class的值: {element.get_attribute('class')}")
print(f"元素是否可见: {element.is_displayed()}")
print(f"元素是否可用: {element.is_enabled()}")
print(f"元素是否被选中: {element.is_selected()}")