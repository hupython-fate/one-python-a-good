from requests import models
from requests import sessions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import os
import time
import urllib.parse as UP
def requests():
    import requests
    req=models.Request()#创建请求对象。
    req.headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive','Referer': 'https://image.baidu.com/'
}
    req.method='GET'
    req.url='https://image.baidu.com/search/index/'
    req.params={'tn': 'baiduimage',
        'word': '雾岛董香',  # 直接使用中文，requests 会自动编码
        'ie': 'utf-8' }
    reprrr=req.prepare()#准备

    sessions1=sessions.Session()
    print("已发送请求。")
    response=sessions1.send(reprrr)#发送
    print("正在等待响应。")

    if response.status_code==200:
        AAA=BeautifulSoup(response.text,'html.parser')
        tag=AAA.find_all('img')
        img_url=[]
        for k in tag:
            m=k.get("src")
            img_url.append(m)
        for l in img_url:
            print(l)
    else:
         print("请求失败，状态码为：",response.status_code)
def selenium(ll='图片目录'):
    if not os.path.exists(ll):
        os.makedirs(ll)
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Edge(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    url='https://image.baidu.com/search/index?tn=baiduimage&word=雾岛董香&ie=utf-8'
    driver.get(url)
    time.sleep(3)
    html=driver.page_source
    AAA=BeautifulSoup(html,'html.parser')
    img_url=AAA.find_all('img')
    url_img=[]
    for n in img_url:
        s=n.get('src')
        if s:
        # 处理各种URL格式
            if s.startswith('//'):
                src = 'https:' + s  # 协议相对URL
            elif s.startswith('/'):
                src = 'https://image.baidu.com' + s  # 绝对路径
            elif not s.startswith(('http://', 'https://')):
                continue  # 跳过无效URL
            url_img.append(s)
    print(f"整理出 {len(url_img)} 个有效的图片URL")

    #下载图片
    session=sessions.Session()
    p=0
    for l,url in enumerate(url_img):
        print(f"正在下载第 {l + 1} 张图片...")
        response = session.get(url, timeout=5)
        if response.status_code == 200:
            # 根据URL确定文件扩展名
            if '.jpg' in url.lower() or 'jpeg' in url.lower():
                ext = '.jpg'
            elif '.png' in url.lower():
                ext = '.png'
            elif '.gif' in url.lower():
                ext = '.gif'
            else:
                ext = '.jpg'  # 默认

            # 生成唯一文件名
            filename = os.path.join(ll, f'图片_{l + 1}{ext}')
            with open(filename, 'wb') as f:
                f.write(response.content)
            p += 1
            print(f"✓ 成功保存: {filename}")
    print(f"下载完成！共成功下载 {p} 张图片")
    driver.quit()
selenium()




