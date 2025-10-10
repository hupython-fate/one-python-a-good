from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

options=Options()
#options.add_argument('--headless')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Edge(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

url='https://www.qidian.com/all/chanId14300-orderId11/'
driver.get(url)
time.sleep(1)

'''
f=driver.find_element(By.ID,'s-box')
f.send_keys('诡秘之主')
#<label id="search-btn" class="search-btn"><em class="iconfont" data-eid="qd_A13"></em></label>
g=driver.find_element(By.ID,'search-btn')
g.click()
'''
#页面自动跳转已经实现了，但是如何自动化获取跳转后的页面的url呢？
#另外，如果起点中文网的搜索是通过AJAX加载结果而不是跳转，那么URL可能不会改变。这种情况下，您需要等待搜索结果区域的加载，而不是等待URL变化。
#如果页面是AJAX加载，您可以等待搜索结果元素出现
#页面没有跳转，才会出现这种情况。
# 等待页面跳转完成
#WebDriverWait(driver, 10).until(EC.url_changes(url))
# 等待URL发生变化
#这行代码表示：等待最多10秒，直到当前URL发生变化（即与初始的url不同）。如果10秒内URL变化了，则继续执行；如果10秒后URL还没变，则抛出异常。


'''如何使页面的url发生变化呢？'''
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 's-box'))
)

# 输入搜索内容
search_box = driver.find_element(By.ID, 's-box')
search_box.clear()
search_box.send_keys('诡秘之主')

# 最可靠的方法：使用回车键
search_box.send_keys(Keys.ENTER)

# 等待跳转
try:
    WebDriverWait(driver, 10).until(
        EC.url_contains("search")
    )
    print("搜索成功！跳转后的URL:", driver.current_url)
except:
    print("可能搜索未成功，当前URL:", driver.current_url)

driver.quit()







# 获取跳转后的URL
current_url = driver.current_url
print(f"跳转后的URL: {current_url}")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
print("搜索结果加载完成")

time.sleep(10)
#html=driver.page_source

ll=driver.find_elements(By.TAG_NAME,'a')
for f in ll:
    print(f.text)

driver.quit()



'''没办法跳转url,获取不到目标数据。'''
