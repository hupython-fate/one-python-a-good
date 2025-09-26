import requests
from bs4 import BeautifulSoup
#导入第三个库，用于模拟浏览器的加载动态网页内容。
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


head={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
url='https://mobile.pinduoduo.com/search_result.html?search_key=%E9%9A%8F%E8%BA%ABwifi&search_type=goods&source=search&options=3&refer_search_met_pos=0&refer_page_el_sn=615206&search_met_track=hot&q_search=%7B%22pes_req_id%22%3A%22d36bff4a-3b84-47e1-bfdf-484808f1a9aa%22%7D&refer_page_name=search_result&refer_page_id=10015_1758876585894_8jt3w14ode&refer_page_sn=10015&page_id=10015_1758876591082_x3pgofjjur&bsch_is_search_mall=&bsch_show_active_page=&flip=0%3B0%3B0%3B0%3B316794b4-67e5-0e68-775f-d6f6fbefd62a%3B%2F20%3B19%3B3%3Bad2ae585a2379f810f45fe89293656d4&sort_type=_sales&price_index=-1&filter=&opt_tag_name=&brand_tab_filter=&item_index=26&is_back=&list_id=mqaqh8gm0e'
fan_hui_de_hui_yin=requests.get(url,headers=head)
print(fan_hui_de_hui_yin)





html=fan_hui_de_hui_yin.text
#print(html)

jie_xi_html=BeautifulSoup(html,'html.parser')
print(jie_xi_html)



#总结，html源代码爬是爬出来了，但是不能获取动态的网页html源代码，
# 也就不能爬到我想要的信息，对使用javaScrpt进行实时渲染的一些网战，根本就毫无用处，但对某些网站，比如说诗词网，甚至不用伪装浏览器。