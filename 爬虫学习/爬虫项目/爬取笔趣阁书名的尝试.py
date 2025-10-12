from selenium import webdriver
#from selenium.webdriver.edge.options import Options
#实际上操作，如果不用配置浏览器，可以省略第二行代码，比如现在的程序。
from bs4 import BeautifulSoup
import re
def bi_qu_ge():
    driver = webdriver.Edge()
    url='https://www.bqgui.cc/'
    driver.get(url)
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    nei_rong=soup.find_all('div',class_='wrap')
    s=str(nei_rong)
    zuo_zhe_ming=r'/">(.*?)</a>'
    zuo_zhe_min1=re.findall(zuo_zhe_ming,s)
    x=1
    for v in zuo_zhe_min1:
        pp = re.findall(r'<(.*?)>', v)
        if pp==[]:
            print(f'书名：{x}',v)
            x=x+1
    driver.quit() #关闭浏览器对象。
bi_qu_ge()
'''面对爬取到的数据中有自己不想要的，可以层层筛选。'''
#真是拍案叫绝，关于添加顺序的解法。
#可以加以完善。方向是添加错误处理和数据存储。