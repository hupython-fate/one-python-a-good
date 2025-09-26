from urllib.request import urlopen
url='https://www.gushicimingju.com/shiren/libai/'
resp=urlopen(url)
#print(resp)
x=resp.read().decode('utf-8')#网页的页面源代码
print(x)
#可以看到返回的内容，带\x的是未还原的中文。
with open('./返回的html文件.html','w',encoding='utf-8') as l:
    l.write(x)


#今天安装了Chrome，了解了服务器渲染和客户端渲然。
#解答了我的很大的疑惑，并且初步了解了web请求的流程。
#什么原因？因为我认真好学，上了up主，python研究社的网课。