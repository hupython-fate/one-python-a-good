from playwright.sync_api import sync_playwright
import requests

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://mobile.pinduoduo.com/search_result.html?search_key=wifi')  # 等待所有JS执行完成

    # 现在能获取完整内容！
   # content = page.query_selector('#root')
   # print(content.text())  # 输出真实的文章内容