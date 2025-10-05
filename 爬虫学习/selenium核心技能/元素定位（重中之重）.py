#Selenium 提供了 8 种主要的定位方式，通过 By 类来使用。

from selenium import webdriver

from selenium.webdriver.common.by import By

driver=webdriver.Edge()

driver.get("https://www.example.com/login")

#value 是什么意思？值： 一个变量或常数所代表的数字、数据或结果。例句： 变量 x 的值是 5。例句： 这个函数的返回值是多少？

# 1,通过ID定位 (最快，最首选)
username_field = driver.find_element(By.ID, "username")

# 2,通过Name定位
search_field = driver.find_element(By.NAME, "q")

# 3,通过Class Name定位
submit_button = driver.find_element(By.CLASS_NAME, "btn-primary")

# 4,通过Tag Name定位
all_links = driver.find_elements(By.TAG_NAME, "a") # 注意：find_elements 返回列表

# 5,通过Link Text定位 (精确匹配链接文本)
login_link = driver.find_element(By.LINK_TEXT, "登录")

# 6,通过Partial Link Text定位 (部分匹配链接文本)
partial_link = driver.find_element(By.PARTIAL_LINK_TEXT, "忘记")

# 7,通过CSS Selector定位 (功能强大，速度快)
# 语法同CSS，.代表class, #代表id
css_element = driver.find_element(By.CSS_SELECTOR, "div.container > form#login-form input[type='text']")

# 8,通过XPath定位 (功能最强大，可以遍历DOM树)
# 绝对路径 (脆弱，不推荐)
xpath_abs = driver.find_element(By.XPATH, "/html/body/div[1]/form/input[1]")
# 相对路径 (推荐)
xpath_rel = driver.find_element(By.XPATH, "//input[@id='username']")
# 使用文本内容
xpath_text = driver.find_element(By.XPATH, "//button[contains(text(),'提交')]")


'''
优先使用 ID、Name。

其次使用 CSS Selector，因为它速度快且语法简洁。

在复杂定位（如根据文本、层级关系）时使用 XPath。

find_element 返回第一个匹配的元素，如果没找到会抛出异常。

find_elements 返回所有匹配元素的列表，如果没找到则返回空列表。
'''