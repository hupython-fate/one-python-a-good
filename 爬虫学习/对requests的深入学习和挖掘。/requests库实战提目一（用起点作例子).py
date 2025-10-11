'''
题目1：请求生命周期追踪
创建一个完整的HTTP请求流程，从构建Request对象开始，
经过prepare()方法转换为PreparedRequest，最终通过Session发送并接收Response。记录每个阶段对象属性的变化。
'''



import requests.models as models
import requests.sessions as sessions
import time



request=models.Request()#models.Request是类名，这是在创建一个request实例。
request.url='https://www.qidian.com/'#添加request的url属性。
request.headers={'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64; x64'}#添加请求头，因为要伪装成普通的浏览器。要是一个字典。
request.data=(None)#添加请求体。因为有一些信息要告知服务器。这里是空，因为是抓取信息。
request.method='GET'  #请求的方法。因为是要爬取起点的数据。
#request.params={'key':'诡秘之主'}   #可以手动添加url参数。
#记住：在Python中，设置对象属性使用赋值操作符（=），而不是像调用函数那样使用括号。



#起求构建完后，就可以把它用prepare()方法转化为PrepareRequests对象。
re=request.prepare()


#准备完后，就可以用sessions模块中的方法发送请求。

sessions1=sessions.Session()#创建一个会话。

response=sessions1.send(re)#send(）方法是发送请求的方法。

'''
我们首先来理解一下models模块中的Response类和sessions模块中send方法返回的Response对象之间的关系。

在requests库中，models.Response类定义了HTTP响应模型，它包含了服务器返回的所有信息，比如状态码、响应头、响应体等。

当我们使用sessions.Session.send()方法发送一个PreparedRequest（预备请求）时，该方法会执行请求，然后构建一个Response对象，并将其返回。

所以，sessions.Session.send()方法返回的resp就是一个models.Response类的实例。

在实际应用中，我们通常不会直接实例化Response对象，而是通过发送请求得到它。然后，我们可以通过这个Response对象来获取服务器返回的数据。

下面我们通过一个简单的例子来说明：

创建一个Request对象，并准备（prepare）它，得到一个PreparedRequest对象。

使用Session的send方法发送这个PreparedRequest对象。

得到Response对象，并从中提取我们需要的信息。
'''



#202的意思是请求成功，但是还没有处理完成。


k=1
while response.status_code!=200:
    response = sessions1.send(re)
    print(f'第{k}次请求，',response.status_code)
    k+=1
print(response.text)

if response.status_code==200:
    print('请求成功！')
    print('如果要进行下一步，可以使用BeautifulSoup.')
else:
    print(response.status_code)
response.colik()




