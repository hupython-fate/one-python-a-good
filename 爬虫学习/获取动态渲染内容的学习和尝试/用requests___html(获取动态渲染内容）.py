import os
from requests_html import HTMLSession
def hh():
    os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'https://npm.taobao.org/mirrors/'
    session = HTMLSession()
    response = session.get('https://movie.douban.com/')
# 关键步骤：渲染JavaScript！
    response.html.render()  # 这会执行JS，等待页面完全加载
# 现在 response.html 包含的是渲染后的完整HTML
# 而且它自带类似BeautifulSoup的解析功能
    titles = response.html.find('h1')  # 直接提取元素
'''我还没有学会requests_html,待学习。'''