from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Edge()

driver.get("https://www.example.com")

# 初始化ActionChains对象
actions = ActionChains(driver)

# 找到需要操作的元素
menu = driver.find_element(By.ID, "menu")
submenu = driver.find_element(By.ID, "submenu")

# 鼠标悬停
actions.move_to_element(menu).perform()

# 点击并按住，然后移动到另一个元素，然后释放 (拖放)
source = driver.find_element(By.ID, "draggable")
target = driver.find_element(By.ID, "droppable")
actions.drag_and_drop(source, target).perform()

# 右键点击
actions.context_click(menu).perform()

# 双击
actions.double_click(menu).perform()

# 组合按键 (例如Ctrl+A)
from selenium.webdriver.common.keys import Keys
text_field = driver.find_element(By.ID, "text-field")
actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()