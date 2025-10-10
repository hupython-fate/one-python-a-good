from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pa_qu(url):
    options=Options()
    options.add_argument('--headless')
    driver=webdriver.Edge(options=options)
    try:
        driver.get(url)

        img=driver.find_elements(By.TAG_NAME,'img')
        img_url=[]
        tu_pian=[]
        w=str(tu_pian)
        for k in img:
            img_url.append(k.text)
        for l in img_url:
            driver.get(l)
            tu=driver.page_source
            tu_pian.append(tu)
        with open('./爬取的图片','w',encoding='utf-8') as h:
            h.write(w)
    except:
        print('发生未知错误，请检查原因。')
    return None

try:
    x=input('请输入url:')
    pa_qu(x)
except:
    print("发生未知错误。")


