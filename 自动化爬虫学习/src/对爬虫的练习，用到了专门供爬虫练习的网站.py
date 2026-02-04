from bs4 import BeautifulSoup
import requests
def pa():
    he={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64)'}#将自己的请求伪装成正常的浏揽器请求。
    response=requests.get('https://books.toscrape.com/',headers=he)#向莫个网url发送请求。
    if response.status_code==200:
        X=response.text#把响应体赋值给莫个变量。
        so=BeautifulSoup(X,'html.parser')#调用BeautifulSoup函数，括号里的第一个参数是从网页获取的html源代码，也就是响应体。
#“html.parser"是表示这个函数是用来解析html源代码的。指定解析器。
        print(so.p)#可以看到这个对象html源代码的第一行<p>标签的内容。
        print(so.img)#可以看到这个对象的第一个img内容。
#每个对象有自己的属性和方法。这个BeautifulSoup也就相当于一个对象。
        yyy=so.find_all('p',class_="price_color" )#返回一个列表。
        print(yyy)
#这是一个示例。
#findAll
#findAll方法的用处是，在成功获取到目标网页的html源代码后，能从巨大的信息堆中，找出我想要的信息。
#这要结合浏览器的检查功能了。
#findAll是一个方法，.前的“so”是对象名，括号内的是要查找的目标。
#p是标签，attrs是属性，两者结合，可以找出对应的元素。
#findAll会返回一个可迭代对象，意思是可以用for循环来依次操作每个对象，一般是一个列表（list)
#接下来可以随机应变的处理找到的信息了。
        for a in yyy:
            print(a.string[2:])#[2:]会返回索引值大于等于2的内容。#这被称为切片操作。
#上面的代码取得了预期的结果。
#下面来获取书名。
        fff=so.find_all('h3')
        for xxx in fff:
            lll=xxx.find_all('a')#此行返回的是一个列表。
            for ilne in lll:
                print(ilne.string)#.string不能对列表使用,只能对单个元素操作。
        #要注意缩进。
    #也可以这样做。
    else:
        print('请求不成功，状态码为：',response.status_code)
    '''
    把lll=xxx.find_all('a')改为lll=xxx.find('a')
    然后，把for ilne in lll: 删掉。
    再把print（ilne.string)中的ilne改为lll.
    '''


#string属性可以把被标签包裹的文字返回，如上。
#如果没有加string属性，就不仅会返回被标签包裹的文字，还会返回标签和标签内的属性。
'''
<某个标签开头  某个属性：“某个与其属性对应的值”>被标签包裹的文字内容<某个标签结尾>
'''

pa()