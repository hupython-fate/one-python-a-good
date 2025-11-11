
from playwright.sync_api import sync_playwright
import time


def login_crawler(login_url, target_url, username, password):
    """处理需要登录的网站"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()


        # 登录流程
        page.goto(login_url)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')

        # 等待登录完成
        page.wait_for_url("**/dashboard**")  # 等待跳转到登录后页面

        # 现在可以访问需要登录的页面
        page.goto(target_url)
        html = page.content()

        # 保存登录状态供下次使用
        page.context.storage_state(path="auth.json")

        browser.close()
        return html