from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import re
import time


def pa_qu(url):
    op=Options()
    op.add_argument("--disable-blink-features=AutomationControlled")
    op.add_experimental_option("excludeSwitches", ["enable-automation"])
    op.add_experimental_option('useAutomationExtension', False)
    op.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    dri=webdriver.Edge(options=op)
    dri.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    dri.get(url)
    time.sleep(10)
    html=dri.page_source
    #现在竟然还要手动分析页面结构，才能从中提取出信息，真是不够自动化，要是能使程序自动分析页面结构，那就好了。
