from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import requests
import time
import os
def pa_qu(url):
    options=Options()
    options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver=webdriver.Edge(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    time.sleep(5)
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    img_tag=soup.find_all('img')
    img_url=[]
    #第一步，获取有效的url.

    for k in img_tag:
        yuan_img_url=k.get('src')
        if yuan_img_url:
                # 处理各种URL格式
            if yuan_img_url.startswith('//'):
                src = 'https:' + yuan_img_url
                    # 协议相对URL
                img_url.append(src)
            elif yuan_img_url.startswith('/'):
                src = 'https://image.baidu.com' + yuan_img_url
                    # 绝对路径
                img_url.append(src)
            elif not yuan_img_url.startswith(('http://', 'https://')):
                continue  # 跳过无效URL
            # startswith()是Python字符串方法，用于检查字符串是否以指定的前缀开头。它返回一个布尔值（True或False）。
            # 需要有一个筛选机制，来把有效url筛选出来。#如上。
    print(f"整理出 {len(img_url)} 个有效的图片URL")
    driver.quit()

    #第二步，下载图片：
    lll='爬到的小说封面图集'
    if not os.path.exists(lll):
        os.makedirs(lll)
    sess=requests.sessions.Session()
    p=0
    for l,ur in enumerate(img_url):
            #每一张图片都要有一个不同的名字。
        print(f"正在下载第{l+1}张图片。")
            #head = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
        response=sess.get(ur,timeout=3)
        if response.status_code==200:
                # 根据URL确定文件扩展名
            if '.jpg' in ur.lower() or 'jpeg' in ur.lower():
                ext = '.jpg'
            elif '.png' in ur.lower():
                ext = '.png'
            elif '.gif' in ur.lower():
                ext = '.gif'
            else:
                ext = '.jpg'  # 默认
                # 生成唯一文件名
            filename = os.path.join(lll, f'图片_{l + 1}{ext}')
            with open(filename,'wb') as h:
                h.write(response.content)
            p += 1
            print(f"✓ 成功保存: {filename}")
        else:
            print('请求失败，状态码为，',response.status_code)
        print(f"下载完成！共成功下载 {p} 张图片")
        time.sleep(1)#防止对服务器造成太大的压力。
    return None
if __name__ == '__main__':
    x='https://www.qidian.com/all/'
    pa_qu(x)