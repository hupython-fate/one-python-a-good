import requests.models as models
import inspect

# 查看模块的所有公共成员
public_members = [name for name in dir(models) if not name.startswith('_')]
print("models模块的公共成员:")
for n in public_members:
    print(n)


#三个重点

#Request
#PreparedRequest
#response


#创建request实例
#request=Request()
#request.url=''#添加请求的url网址。
#request.data={}


# 查看Request类的所有方法
request_methods = [method for method in dir(models.Request)
                  if not method.startswith('_')]#列表表达式。
print("Request类的方法:", request_methods)

# 创建Request实例并探索
req = models.Request()
print("\nRequest实例的属性:")
for attr in dir(req):
    if not attr.startswith('_'):
        value = getattr(req, attr)
        print(f"  {attr}: {type(value)} = {value}")

'''
Request类的重要属性：

method - HTTP方法（GET, POST等）

url - 请求URL

headers - 请求头

data - 请求体数据

json - JSON数据

params - URL参数

auth - 认证信息

cookies - Cookies

hooks - 钩子函数
'''

# 查看PreparedRequest类的方法
prepared_methods = [method for method in dir(models.PreparedRequest)
                   if not method.startswith('_')]
print("\nPreparedRequest类的方法:", prepared_methods)

# 从Request创建PreparedRequest
try:
    req = models.Request()
    req.method = 'POST'
    req.url = 'https://httpbin.org/post'
    req.data = {'key': 'value'}
    req.headers = {'User-Agent': 'my-app'}
except:
    print("发生错误。")

prepped = req.prepare()#工产方法，返回PreparedRequest实例。
print("\n预备请求的关键属性:")
print(f"方法: {prepped.method}")
print(f"URL: {prepped.url}")
print(f"头信息: {prepped.headers}")
print(f"体数据: {prepped.body}")
'''
PreparedRequest的重要特点：

不可变对象，一旦创建就不能修改

所有数据都已编码为字节

头信息已完全生成

'''




我们关注的是 requests.models.Response 类，它是 HTTP 响应的封装。下面列出其主要的属性和方法。

属性
status_code：HTTP 状态码，如 200、404 等。

headers：响应头的字典，但不区分大小写。

url：最终请求的 URL（考虑重定向）。

history：响应历史列表（重定向），包含之前请求的 Response 对象。

reason：响应状态的原因短语，如 "OK"、"Not Found"。

cookies：服务器设置的 Cookie，是一个 RequestsCookieJar 对象。

elapsed：请求消耗的时间，是一个 timedelta 对象。

request：对应的 PreparedRequest 对象（即发送的请求）。

connection：用于响应的连接适配器（内部使用）。

raw：原始的响应对象（通常是 urllib3 的 HTTPResponse）。

content：响应内容的字节形式。

text：响应内容的字符串形式（根据响应编码解码）。

encoding：响应编码，用于解码 content 成 text。

apparent_encoding：通过chardet库检测的编码。

is_redirect：是否重定向。

is_permanent_redirect：是否永久重定向。

next：重定向链中的下一个请求（如果有）。

links：响应头中的链接头解析（如果有）。

方法
json(kwargs)**：将响应内容解析为 JSON。kwargs 会传递给 json.loads。

raise_for_status()：如果状态码表示错误（4xx 或 5xx），则抛出 HTTPError 异常。

iter_content(chunk_size=1, decode_unicode=False)：迭代响应内容，每次返回指定大小的字节（或解码后的字符串）。用于处理大响应。

iter_lines(chunk_size=512, decode_unicode=False, delimiter=None)：迭代响应内容，按行返回。

close()：关闭响应，释放底层连接回连接池。

说明
大多数属性是在响应被发送后填充的。

使用 iter_content 和 iter_lines 可以流式处理大响应，避免一次性加载到内存。
