import requests
from bs4 import BeautifulSoup
#导入第三个库，用于模拟浏览器的加载动态网页内容。
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

def pa_pin_duo():
    options=Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 模拟真实用户
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Edge(options=options)

    # 执行JavaScript移除webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



#key=input('你想要查询的商品：')
    url='https://mobile.pinduoduo.com/search_result.html?search_key=wifi'
    driver.get(url)
    time.sleep(60)
    html=driver.page_source
    jie_xi_html=BeautifulSoup(html,'html.parser')#解析后的响应体。
#print(jie_xi_html)
#all_cookies = driver.get_cookies()
#for cookie in all_cookies:
 #   print(f"{cookie['name']} -> {cookie['value']}")
#总结，html源代码爬是爬出来了，但是不能获取动态的网页html源代码，
# 也就不能爬到我想要的信息，对使用javaScrpt进行实时渲染的一些网战，根本就毫无用处，但对某些网站，比如说诗词网，甚至不用伪装浏览器。
#用selenium解决了动态渲染的问题。
#新的问题是，登录问题。
#手动登录的话，又有可能网络繁满。？？这到底是反爬机制还是真的网络问题？
#是反爬机制。

#也许用selenium中的元素交互的知识和requests中的sessions模块，可以解决。