import asyncio
import aiohttp# 异步版 requests，基于 asyncio
from bs4 import BeautifulSoup

async def fetch_title(session, url):#第一个协程函数，返回一个协程对象。
    #async def 不是普通函数，它返回一个协程对象；只有前面加await 才真正运行。
    #参数里的session相当于requests.Session()，但必须复用，否则并发优势全没。
    try:
        async with session.get(url, timeout=10) as resp:
            #async with 保证连接用完放回连接池；timeout=10 防止某些页面卡死整个程序；
            # 如果你写成 requests.get(..., timeout=10) 效果类似，但这里不会阻塞线程。
            text = await resp.text()
            soup = BeautifulSoup(text, 'lxml')
            title = soup.title.string if soup.title else 'No Title'
            #await resp.text()是唯一会“等”的地方；事件循环趁它等网络时切到别的协程。
            #后面BeautifulSoup的用法跟你以前一模一样，所以你把旧代码直接搬进来即可。
            print(f'{url} -> {title.strip()}')
            return title
    except Exception as e:
        print(f'Error fetching {url}: {e}')
        return None
    #异步里一旦抛异常没捕获，整个 gather 会直接把其余任务全取消；所以务必把可能出错的 IO 包一层 try/except；
#生产环境可换成 asyncio.TimeoutError, aiohttp.ClientError 更精细
async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_title(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    urls = [
        'https://example.com',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/3',
    ]
    asyncio.run(main(urls))