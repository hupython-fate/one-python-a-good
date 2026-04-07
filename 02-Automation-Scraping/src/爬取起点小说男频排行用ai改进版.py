from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json


def get_rank_books():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    url = 'https://www.qidian.com/rank/'
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)

    # 等待榜单加载完成（等待至少一个第一名条目出现）
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.unfold"))
        )
    except:
        time.sleep(5)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    # 所有榜单的第一名条目（class="unfold"）
    top_items = soup.select('li.unfold')

    books = {}  # 书名 -> 作者
    seen_titles = set()

    for item in top_items:
        # 提取书名
        h2 = item.find('h2')
        if not h2:
            continue
        title_tag = h2.find('a')
        if not title_tag:
            continue
        title = title_tag.get_text().strip()

        # 提取作者
        author_tag = item.select_one('p.author a.writer')
        author = author_tag.get_text().strip() if author_tag else "未知作者"

        if title not in seen_titles:
            seen_titles.add(title)
            books[title] = author
            print(f"书名：{title}，作者：{author}")

    # 保存为文本文件（制表符分隔）
    '''
    with open('起点排行榜_榜首.txt', 'w', encoding='utf-8') as f:
        f.write("书名\t作者\n")
        for title, author in books.items():
            f.write(f"{title}\t{author}\n")
    '''

    # 同时保存 JSON 格式
    with open('4月起点排行榜_榜首.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    print(f"\n共获取 {len(books)} 本榜首书籍")


if __name__ == "__main__":
    get_rank_books()