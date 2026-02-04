import asyncio
import requests
from bs4 import BeautifulSoup
async def PA():
    url='https://www.qidian.com/'
    he = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
    session=requests.Session()
    response=session.get(url,headers=he)
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'html.parser')
        book_title=[]
        tag_a=soup.find_all("a")
        for sting in tag_a:
            book_title.append(sting.string)
        print(f"共收集到{len(book_title)}本书的书名。")
    else:
        while response.status_code!=200:
            response = requests.get(url, headers=he)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                book_title = []
                tag_a = soup.find_all("a")
                for sting in tag_a:
                    book_title.append(sting.string)
                print(f"共收集到{len(book_title)}本书的书名。")
            else:
                print("请求未成功，状态码为，",response.status_code)
async def PA_1():
    url="https://www.qdmm.com/"
    he = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}
    response=requests.get(url,headers=he)
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'html.parser')
        book_title=[]
        tag_a=soup.find_all("a")
        for sting in tag_a:
            book_title.append(sting.string)
        print(f"共收集到{len(book_title)}本书的书名。")
    else:
        while response.status_code!=200:
            response = requests.get(url, headers=he)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                book_title = []
                tag_a = soup.find_all("a")
                for sting in tag_a:
                    book_title.append(sting.string)
                print(f"共收集到{len(book_title)}本书的书名。")
            else:
                print("请求未成功，状态码为，",response.status_code)
async def AAAA():
    task1=asyncio.create_task(PA())
    task2=asyncio.create_task(PA_1())
    await task1
    await task2
asyncio.run(AAAA())
'''这不是真正的异步编程！ 你的代码存在几个关键问题：
requests 是同步HTTP库，它会阻塞事件循环，即使放在 async 函数中也不会变成异步
虽然函数声明为 async，但内部全是同步操作。
async def AAAA():
    task1 = asyncio.create_task(PA())  # 实际上还是顺序执行
    task2 = asyncio.create_task(PA_1())
    await task1  # 这里会阻塞等待 PA() 完成
    await task2  # 然后才执行 PA_1()
    
    这个代码：

✅ 语法上是异步的（用了 async/await）

❌ 但实际上还是同步执行

❌ 没有利用异步并发的优势
    '''




