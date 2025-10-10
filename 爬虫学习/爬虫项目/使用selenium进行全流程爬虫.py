from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time

options=Options()
options.add_argument('--headless')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Edge(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

url='https://movie.douban.com/annual/2024/?fullscreen=1&dt_from=movie_navigation'
driver.get(url)
time.sleep(5)
html=driver.page_source

#本来下一步就是用BeautifulSoup或者re进行解析和信息提取了，但是因为是用selenium进行全流程爬虫，所以用By类的方法或函数。
move=[]
u = driver.find_elements(By.TAG_NAME,'a')
for c in u:
    move.append(c.text)#要使用.text才能获得文本内容。
s=str(move)#转化为能存储得数据类型。
'''
也可以使用get_attribute() 方法

u = driver.find_element(By.TAG_NAME, "a")
print(u.get_attribute("textContent"))  # 获取所有文本内容（包括隐藏的）
print(u.get_attribute("innerText"))    # 获取可见文本内容
print(u.get_attribute("innerHTML"))    # 获取包含HTML标签的内容
'''

'''
总结
要获取元素的文本内容，记住这几点：

使用 .text 属性 - 获取可见文本

使用 get_attribute() - 获取各种属性内容

find_element() 返回的是对象 - 需要进一步操作才能获取文本

检查元素是否可见 - 不可见的元素可能有空文本
'''
with open('./2024年优秀电影名单.txt','w',encoding='utf-8')as gg:
    gg.write(s)


#可以完全使用Selenium的By类来定位和提取数据，无需切换到BeautifulSoup或re了！