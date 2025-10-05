from selenium import webdriver
from selenium.webdriver.common.by import By
driver=webdriver.Edge()

#a,强制等待：
import time
time.sleep(5) # 无条件等待5秒


#b,隐性等待：
#为整个 driver 的会话设置一个全局的等待时间，在查找任何元素时，如果元素没有立即出现，会轮询等待，直到超时。

driver.implicitly_wait(10) # 设置隐式等待10秒
# 后续所有的 find_element 操作都会最多等待10秒
element = driver.find_element(By.ID, "dynamic-element")


#c,显性等待：
#针对特定条件进行等待，更加灵活和高效。它使用 WebDriverWait 和 expected_conditions。
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e

# 设置显式等待，最多等10秒，每0.5秒检查一次条件
wait = WebDriverWait(driver, 10)

# 等待元素出现在DOM中并可见
elements= wait.until(e.visibility_of_element_located((By.ID, "dynamic-element")))

# 等待元素可被点击
clickable_element = wait.until(e.element_to_be_clickable((By.ID, "submit-btn")))
clickable_element.click()

# 等待元素从DOM中消失
wait.until(e.invisibility_of_element_located((By.ID, "loading-spinner")))

# 等待页面标题包含特定文本
wait.until(e.title_contains("订单完成"))

# 其他常用条件：
# presence_of_element_located - 元素出现在DOM中（不一定可见）
# text_to_be_present_in_element - 元素中包含特定文本
# alert_is_present - 出现警报框
