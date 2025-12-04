from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Edge()


#a) 框架 (iframe)
driver.get("https://www.example.com")

# 通过ID、Name或索引切换到框架
driver.switch_to.frame("iframe-name-or-id")
# driver.switch_to.frame(0) # 通过索引（从0开始）

# 在框架内进行操作
frame_element = driver.find_element(By.TAG_NAME, "body")
print(frame_element.text)

# 切回主文档
driver.switch_to.default_content()

# 切回父级框架
driver.switch_to.parent_frame()





#b) 窗口和标签页
# 获取当前窗口句柄
main_window = driver.current_window_handle
print(f"主窗口句柄: {main_window}")

# 点击一个会打开新窗口的链接
driver.find_element(By.LINK_TEXT, "打开新窗口").click()

# 获取所有窗口句柄
all_handles = driver.window_handles
print(f"所有窗口句柄: {all_handles}")

# 切换到新窗口
for handle in all_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break

# 在新窗口操作
print(f"新窗口标题: {driver.title}")

# 关闭新窗口并切回主窗口
driver.close()
driver.switch_to.window(main_window)







#c) 弹出框 (Alert)



# 触发一个警报框
driver.find_element(By.ID, "trigger-alert").click()

# 切换到警报框
alert = driver.switch_to.alert

# 获取警报文本
print(alert.text)

# 接受警报 (点击"确定")
alert.accept()

# 取消警报 (点击"取消")
# alert.dismiss()

# 在提示框(Prompt)中输入文本
# alert.send_keys("这是输入的文字")
# alert.accept()