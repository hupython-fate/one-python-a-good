
import requests.models as models
import requests.sessions as sessions


def pa_yi():
    '''目标是爬取一张图片'''
    req=models.Request()
    req.method='GET'
    req.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    req.url='https://img1.baidu.com/it/u=2651128509,3759062648&fm=253&fmt=auto&app=138&f=JPEG '
    resp=req.prepare()
    session=sessions.Session()
    response=session.send(resp)

    if response.status_code==200:
        with open('一张图片.jpg', 'wb') as f:
            f.write(response.content)
    else:
        print(response.status_code)

pa_yi()