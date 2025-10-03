
'''
任务要求：

1，抓取网址：https://httpbin.org/xml （这是一个返回XML数据的测试页）

2，从返回的XML数据中，提取第一个 <slide> 标签的 type 属性的值。

'''
import requests
import re

#x=input('请输入你要爬取的网站地址：')
#y=input('请输入你想要查询的内容(正则表达式的形式)：')

def yi_ge_can_shi(url,mou_shi):
    headers={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
    resp=requests.get(url,headers=headers)
    print('状态码为（如果是200则说明请求成功）：',resp.status_code)

    # 添加调试信息
    print("=== 调试信息 ===")
    print("正则表达式模式:", mou_shi)
    print("响应内容长度:", len(resp.text))
    print("响应内容前200字符:", resp.text[:200])

    if resp.status_code==200:
        x=re.findall(mou_shi,resp.text)
        print("匹配结果:", x)  # 直接打印匹配结果

        if x==[]:
            print('您想要查找的内容不存在，或输入的正则表达式出现了问题，请您重新运行程序。')
            h=int(input('如果想要查看完整的响应体源代码，请输入1：'))
            if h==1:
                print(resp.text)
        else:
            print(x)
    else:
        print('您的请求未成功，请重新尝试。')
    return resp


y=r'type="(.*?)"'
x='https://httpbin.org/xml'
yi_ge_can_shi(x,y)

# 测试2：通过input获取（模拟你失败的情况）
print("测试2: 通过input调用")
user_url = input('请输入URL（直接回车使用默认）: ') or 'https://httpbin.org/xml'
user_pattern = input('请输入正则模式: ') or r'type="(.*?)"'
result2 = yi_ge_can_shi(user_url, user_pattern)



url='https://httpbin.org/xml'
headers={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
resp=requests.get(url,headers=headers)
#print(resp)
ppp=r'type="(.*?)"'
dd=re.findall(ppp,resp.text)
#print(dd)



'''问题反思：既然单独测试能成功，但在函数中失败，说明问题出在参数传递或环境差异上。'''