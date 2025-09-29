# 安装 playwright 库
#

# 安装所需的浏览器（Chromium, Firefox, WebKit）
#playwright install


#pip install requests-html

from playwright.sync_api import sync_playwright
import time


def simple_crawler(url):
    """最简单的Playwright爬虫"""
    with sync_playwright() as p:
        # 启动浏览器（显示界面以便观察）
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print(f"正在访问: {url}")
        page.goto(url)

        # 等待页面加载
        time.sleep(3)

        # 获取渲染后的完整HTML
        html_content = page.content()
        print("成功获取渲染后HTML!")

        # 截图验证
        page.screenshot(path="page_screenshot.png")
        print("已保存截图: page_screenshot.png")

        # 关闭浏览器
        browser.close()

        return html_content


# 测试
if __name__ == "__main__":
    test_url = "https://mobile.pinduoduo.com/search_result.html?search_key=wifi"  # 先用这个测试网站
    html = simple_crawler(test_url)
    print(f"获取到的HTML长度: {len(html)} 字符")