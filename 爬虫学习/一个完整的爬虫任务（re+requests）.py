
'''
任务要求：

1，抓取网址：https://httpbin.org/xml （这是一个返回XML数据的测试页）

2，从返回的XML数据中，提取第一个 <slide> 标签的 type 属性的值。

'''
import requests
import re
url=input('请输入你要爬取的网站：')

def yi_ge_can_shi(url,mou_shi,headers):
    resp=requests.get(url,headers=headers)
    print('状态码为（如果是200则说明请求成功）：',resp.status_code)
    if resp.status_code==200:

    else:
        print('您')