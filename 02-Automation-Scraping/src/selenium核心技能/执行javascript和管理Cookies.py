from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Edge()


#7. 执行 JavaScript
#当 WebDriver 原生方法无法实现某些操作时，可以借助 JavaScript。
driver.get("https://www.example.com")

# 执行简单的JS
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 滚动到页面底部

# 执行带参数的JS，并获取返回值
element = driver.find_element(By.ID, "some-element")
border_color = driver.execute_script("return arguments[0].style.borderColor;", element)
print(border_color)

# 高亮显示一个元素（调试用）
driver.execute_script("arguments[0].style.border='3px solid red'", element)

# 直接通过JS点击元素（绕过前端事件检测）
driver.execute_script("arguments[0].click();", element)








#8. Cookies 管理
driver.get("https://www.example.com")

# 获取所有cookies
all_cookies = driver.get_cookies()
for cookie in all_cookies:
    print(f"{cookie['name']} -> {cookie['value']}")

# 按名称获取特定cookie
cookie = driver.get_cookie("session_id")

# 添加一个cookie
driver.add_cookie({
    'name': 'my_cookie',
    'value': '12345',
    'domain': 'example.com'
})

# 删除特定cookie
driver.delete_cookie("my_cookie")

# 删除所有cookies
driver.delete_all_cookies()