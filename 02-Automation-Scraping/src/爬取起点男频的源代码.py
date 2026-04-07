from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def save_page_source():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    url = ' https://www.qidian.com//www.qidian.com/rank/hotsales/ '
    driver = webdriver.Chrome(options=options)  # 改为 Chrome
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)

    time.sleep(8)  # 等待页面完全加载
    html = driver.page_source
    driver.quit()

    with open('qidian_rank_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("页面源代码已保存为 qidian_rank_page.html")


if __name__ == "__main__":
    save_page_source()