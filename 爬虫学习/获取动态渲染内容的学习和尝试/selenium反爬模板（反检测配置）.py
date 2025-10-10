from selenium import webdriver
from selenium.webdriver.edge.options import Options
#from selenium.webdriver.common.by import By
import time


def setup_stealth_driver():
    """配置反检测的浏览器驱动"""
    options = Options()#选项的意思

    # 反检测配置
    #argument (字符串): 要添加的命令行参数，以双横线（--）开头，例如 --headless。
    #add_argument() 翻译为："添加_命令行参数"
    #add_experimental_option() 翻译为："添加_实验性_选项"
    '''
    参数说明：

name (字符串): 选项名称

"prefs" - 浏览器偏好设置

"excludeSwitches" - 要排除的浏览器开关

"mobileEmulation" - 移动设备模拟

"detach" - 浏览器分离设置

value (对象): 选项值，类型取决于选项名称

对于 "prefs": 字典类型

对于 "excludeSwitches": 列表类型

对于 "mobileEmulation": 字典类型
    '''
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
    options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Edge(options=options)

    # 执行JavaScript移除webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#execute_script() 翻译为："执行JavaScript脚本"
    return driver


# 使用反检测配置
driver = setup_stealth_driver()
try:
    driver.get('https://www.qidian.com/rank/')
    time.sleep(3)  # 等待页面加载

    # 检查是否成功绕过检测
    if "captcha" not in driver.page_source.lower():#lower() 翻译为："转换为小写"
        print("成功绕过检测!")
        print(driver.page_source[:1000])  # 打印前1000字符查看 #切片操作
    else:
        print("仍然被检测到，需要更高级的方案")

finally:
    driver.quit()