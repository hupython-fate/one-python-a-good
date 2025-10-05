from selenium import webdriver


driver = webdriver.Edge()#创建一个浏览器实例。

# 打开URL
driver.get("https://www.example.com")

# 获取当前标题和URL
print(f"页面标题: {driver.title}")
print(f"当前URL: {driver.current_url}")

# 浏览器导航
driver.back()    # 后退
driver.forward() # 前进
driver.refresh() # 刷新

# 窗口管理
driver.maximize_window() # 最大化
driver.minimize_window() # 最小化
driver.fullscreen_window() # 全屏

# 获取窗口尺寸
print(driver.get_window_size())

# 设置窗口尺寸
driver.set_window_size(1024, 768)

driver.quit()#关闭浏览器