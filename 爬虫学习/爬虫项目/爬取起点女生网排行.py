from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import re
def nv_sheng(url):
    options=Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver=webdriver.Edge(options=options)
# 执行JavaScript移除webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    time.sleep(4)
    html=driver.page_source
    mou_shi=r'<h2>(.*?)</h2>'
    f=re.findall(mou_shi,html)#有重复的，且有杂乱信息的。
    s=set(f)#去重
    book_title=[]
    y=1
    for x in s:
        mou_shi2=r'<(.*?)>'
        dd=re.findall(mou_shi2,x)
        if not dd:
            book_title.append(f'书名：{y}，{x}')#去杂。
            y+=1
    driver.quit()
    ff=str(book_title)
    return ff
#我明白您的问题了！您的代码只能返回最后一行是因为在循环中，每次迭代都会覆盖 vs 变量，最终只保留了最后一个值。
#您需要创建一个列表来存储所有的结果：如上
url = 'https://www.qdmm.com/rank/'
fg=nv_sheng(url)
print(fg)
with open('./2025年10月起点女生高分书排行榜.txt','w',encoding='utf-8') as j:
    j.write(fg)
