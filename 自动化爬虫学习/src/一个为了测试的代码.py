from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Edge(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

url = 'https://www.qidian.com/all/chanId14300-orderId11/'
driver.get(url)

print("页面已加载，当前URL:", driver.current_url)

# 等待搜索框加载
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 's-box'))
)
print("搜索框已找到")

# 输入搜索内容
search_box = driver.find_element(By.ID, 's-box')
search_box.clear()
search_box.send_keys('诡秘之主')
print("已输入搜索关键词")

# 查找所有可能的搜索按钮
print("尝试查找搜索按钮...")
buttons = driver.find_elements(By.TAG_NAME, 'label')
print(f"找到 {len(buttons)} 个label元素")

for i, button in enumerate(buttons):
    print(f"Label {i}: 文本='{button.text}', for属性='{button.get_attribute('for')}'")

# 尝试点击正确的按钮
try:
    search_button = driver.find_element(By.CSS_SELECTOR, 'label[for="s-box"]')
    print("找到搜索按钮，准备点击")
    search_button.click()
    print("已点击搜索按钮")
except Exception as e:
    print(f"点击失败: {e}")

# 等待可能的跳转
time.sleep(3)
print("等待后的URL:", driver.current_url)

# 检查是否跳转
if driver.current_url != url:
    print("页面已跳转!")
    print(f"新URL: {driver.current_url}")
else:
    print("页面未跳转，尝试其他方法...")
    # 可以在这里添加其他尝试方法

driver.quit()