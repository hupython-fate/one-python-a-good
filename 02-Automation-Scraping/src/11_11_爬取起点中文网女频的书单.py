from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
#如果你听网课感觉到困倦,这说明你该动手实践了.
#写会代吗,精神百倍.

chrome_options = Options()

# 新增：隐藏自动化特征（核心配置）                                                                                     
chrome_options.add_argument("--disable-blink-features=AutomationControlled")                                        
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])


service = Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service,options=chrome_options) #创建浏览器对象.
# 新增：移除navigator.webdriver属性
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

url_1="https://www.qdmm.com/rank/"#起点女生网的网址
url_2="https://www.baidu.com/"
driver.get(url_1)

#ime.sleep(15)#强制等待,没有技术含量.
driver.implicitly_wait(20)#隐性等待,有技术含量,如果元素提前出现了,那么就会结束等待.

driver.maximize_window() #页面最大化.
time.sleep(5)
#html=driver.page_source

#print(html)
#这个代吗不能成功,因为网站检测到浏览器被自动化程序控制..
driver.quit()

'''
这3行配置的作用（简单理解）

    --disable-blink-features=AutomationControlled

        告诉浏览器：不要显示"正受到自动测试软件的控制"

    excludeSwitches, ["enable-automation"]

        隐藏Chrome的自动化标志

    execute_script 那一行

        让网站检测不到你在用Selenium

'''
