import json
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# ========== 在这里粘贴你从控制台复制的 cookie 字符串 ==========
COOKIE_STRING = "newstatisticUUID=1775572701_484065043; traffic_utm_referer=; fu=19741327; supportwebp=true; Hm_lvt_f00f67093ce2f38f215010b699629083=1775572705,1775572943; Hm_lpvt_f00f67093ce2f38f215010b699629083=1775572943; HMACCOUNT=31BB6D619AD8B226; _csrfToken=DyMC8w1zSnAxaXO0ZVggQTDYNY4OkpvqSYOLeSfb; ywkey=ywyNkXdDC90c; ywguid=855095663520; e1=%7B%22l6%22%3A%22%22%2C%22l7%22%3A%22%22%2C%22l1%22%3A3%2C%22l3%22%3A%22%22%2C%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_A1004%22%7D; e2=%7B%22l6%22%3A%22%22%2C%22l7%22%3A%22%22%2C%22l1%22%3A3%2C%22l3%22%3A%22%22%2C%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_A1003%22%7D"  # 在这里填入你登录后的 cookie


# 例如 "qd_p=xxxxx; qd_uuid=yyyyy; ..."


# ========================================================

def add_cookies_from_string(driver, cookie_str, domain='.qidian.com'):
    """将 cookie 字符串添加到 driver 中"""
    if not cookie_str:
        return
    for item in cookie_str.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' in item:
            key, value = item.split('=', 1)
            # 忽略一些可能导致问题的 cookie 属性
            if key.lower() in ('domain', 'path', 'expires', 'max-age', 'secure', 'httponly'):
                continue
            driver.add_cookie({'name': key, 'value': value, 'domain': domain})


def get_rank_links_from_main(driver, main_url):
    """从主页面解析出所有榜单的独立链接（正确拼接 URL）"""
    driver.get(main_url)
    # 等待页面加载完成
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.rank-list .more'))
        )
    except:
        time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    more_links = set()

    for a in soup.select('.rank-list .more, .rank-list.sort-list .more, .rank-list.mr0 .more'):
        href = a.get('href')
        if href:
            # 使用 urljoin 自动处理相对路径和绝对路径
            full_url = urljoin(main_url, href)
            # 去除可能的重复域名（例如 https://www.qidian.com/https://...）
            if full_url.startswith('https://www.qidian.com/https://'):
                full_url = full_url.replace('https://www.qidian.com/https://', 'https://')
            more_links.add(full_url)

    return list(more_links)


def parse_rank_page(driver, url):
    """解析单个榜单页面，返回 {书名: 作者} 字典"""
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.rank-view-list li, .book-list li'))
        )
    except:
        time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    books = {}

    items = soup.select('.rank-view-list li, .book-list li')
    if not items:
        items = soup.select('.rank-list li')

    for item in items:
        title_tag = item.select_one('h2 a, .name a')
        if not title_tag:
            continue
        title = title_tag.get_text().strip()
        if not title:
            continue

        author_tag = item.select_one('p.author a.writer, .author .writer, .writer')
        if not author_tag:
            author_tag = item.select_one('a[href*="/author/"]')
        author = author_tag.get_text().strip() if author_tag else "未知作者"

        books[title] = author

    return books


def crawl_all_rank_books():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    main_url = 'https://www.qidian.com/rank/'
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # 1. 先访问一次主页，建立域名会话
        driver.get(main_url)
        time.sleep(2)

        # 2. 添加 cookie
        if COOKIE_STRING:
            add_cookies_from_string(driver, COOKIE_STRING)
            # 刷新页面使 cookie 生效
            driver.refresh()
            time.sleep(3)
        else:
            print("警告：COOKIE_STRING 为空，请先填入你的登录 cookie")
            return

        # 3. 获取所有榜单链接
        rank_links = get_rank_links_from_main(driver, main_url)
        print(f"发现 {len(rank_links)} 个独立榜单：")
        for link in rank_links:
            print(f"  {link}")

        all_books = {}
        for idx, link in enumerate(rank_links, 1):
            print(f"\n[{idx}/{len(rank_links)}] 正在爬取: {link}")
            try:
                books = parse_rank_page(driver, link)
                print(f"  获取到 {len(books)} 本书")
                all_books.update(books)
                time.sleep(2)
            except Exception as e:
                print(f"  爬取失败: {e}")

        print(f"\n总共去重后得到 {len(all_books)} 本不同书籍")

        # 保存结果
        '''
        with open('起点所有榜单书籍_书名作者.txt', 'w', encoding='utf-8') as f:
            f.write("书名\t作者\n")
            for title, author in all_books.items():
                f.write(f"{title}\t{author}\n")
        '''

        with open('../爬来的素材/4月起点所有榜单书籍_书名作者.json', 'w', encoding='utf-8') as f:
            json.dump(all_books, f, ensure_ascii=False, indent=2)

        print("保存完成：起点所有榜单书籍_书名作者.txt 和 .json")

    finally:
        driver.quit()


if __name__ == "__main__":
    crawl_all_rank_books()

    '''
     如果以后又出现 0 本书

可能的原因及解决办法：

    Cookie 过期 → 重新复制登录后的 document.cookie
    
    先登陆这个网站。
    在控制台先输入这个allow pasting，
    然后输入这个document.cookie

    页面结构改版 → 需要调整 CSS 选择器（可以再联系我帮你分析）

    反爬升级 → 可以尝试使用 undetected-chromedriver 库（pip install undetected-chromedriver），
    替换 webdriver.Chrome 为 undetected_chromedriver.Chrome
    
    
    '''