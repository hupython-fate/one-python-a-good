'''WebDriverWait - 显式等待控制器
WebDriverWait 是一个类，用于创建等待条件，它会智能地等待某个特定条件成立后再继续执行代码，而不是简单地固定等待一段时间。

基本语法：
WebDriverWait(driver, timeout).until(条件)
driver: 浏览器驱动实例

timeout: 最大等待时间（秒）

条件: 等待的条件，通常来自 EC 模块

expected_conditions (EC) - 预期条件模块
EC 提供了许多预定义的等待条件，常用的包括：

1. 元素可见性相关
python
# 等待元素在页面上可见并可交互
EC.visibility_of_element_located((By.ID, "element_id"))

# 等待元素在DOM中存在（不一定可见）
EC.presence_of_element_located((By.CLASS_NAME, "some_class"))
2. 页面状态相关
python
# 等待URL发生变化（页面跳转）
EC.url_changes("original_url")

# 等待URL包含特定文本
EC.url_contains("keyword")

# 等待页面标题包含特定文本
EC.title_contains("预期标题")
3. 元素可交互性
python
# 等待元素可点击
EC.element_to_be_clickable((By.XPATH, "//button"))
4. 元素状态
python
# 等待元素被选中（如复选框）
EC.element_to_be_selected((By.ID, "checkbox"))

# 等待元素包含特定文本
EC.text_to_be_present_in_element((By.TAG_NAME, "div"), "预期文本")
'''