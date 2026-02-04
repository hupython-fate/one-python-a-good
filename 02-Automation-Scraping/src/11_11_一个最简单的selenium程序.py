from selenium import webdriver
import time
driver=webdriver.Chrome() #启动,创建webdriver对象
driver.get("https://www.bing.com/") #使用get方法
time.sleep(5)
driver.quit()  #使用quit方法,关闭浏览器.

