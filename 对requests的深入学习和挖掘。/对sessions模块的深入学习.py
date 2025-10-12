'''

Requests库中的`sessions`模块是我们处理HTTP请求时的一个强大工具，尤其适合处理需要保持特定状态或进行多次请求的场景。下面我们详细解析它。

### 理解 Session 的核心作用

想象一下，Session就像一个虚拟的浏览器标签页。当你在这个标签页中登录网站后，后续的操作（如访问个人主页）通常会保持登录状态。
RequestsSession的作用类似： ** 在多次请求间保持某些参数和状态 **。

它的两个主要优势是：

1. ** 连接复用 **：Session
对象内部使用了 ** 连接池 **。当向同一主机发送多个请求时，底层的TCP连接会被复用，避免了频繁建立和断开连接的开销，从而显著提升性能。
2. ** 状态保持 **：Session
可以跨请求自动保持cookies等信息。这在处理需要登录的网站时非常方便。

### 🛠️ Session 对象的创建与配置

使用
Session
的第一步是创建它：
'''

import requests

# 创建 Session 对象
session = requests.Session()#requests.Sessions是类名，

'''
你可以为Session预设一些 ** 默认参数 **，这些参数会应用于该Session发出的所有请求：

'''
# 设置默认请求头
session.headers.update({'User-Agent': 'my-app/0.0.1'})

# 设置认证信息
session.auth = ('user', 'pass')

# 设置代理
session.proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

'''

我们通常说的代理，是指网络代理，即客户端不直接连接目标服务器，而是通过一个中间服务器（代理服务器）来转发请求和响应。在requests中设置代理，就是告诉requests库将请求发送到代理服务器，由代理服务器去获取目标服务器的响应，然后代理服务器再将响应返回给客户端。

使用代理的主要目的包括：

隐藏客户端的真实IP地址，保护隐私。

绕过网络限制（如防火墙、IP封锁等）。

访问在特定地区受限的内容（地理封锁）。

进行网络调试和监控。

在requests中，可以通过给请求传递proxies参数来设置代理。proxies参数是一个字典，键是协议（如'http', 'https'），值是代理服务器的地址。

例如：
proxies = {
'http': 'http://10.10.1.10:3128',
'https': 'http://10.10.1.10:1080',

** 使用方法级参数 ** 时，需要注意方法层的参数会覆盖会话层的同名参数。
如果想在某个请求中 ** 移除 ** 会话层设置的某个头，
只需在该请求的方法层参数中将该值设为
`None`。
'''



```python
# 这个请求会发送 'User-Agent': 'my-app/0.0.1'
response1 = session.get('https://httpbin.org/headers')

# 这个请求会发送 'User-Agent': 'other-agent'，因为方法层参数覆盖了会话层参数
response2 = session.get('https://httpbin.org/headers', headers={'User-Agent': 'other-agent'})

# 这个请求不会发送 'x-test' 头，因为它在方法层被设置为 None
response3 = session.get('https://httpbin.org/headers', headers={'x-test': None})
```
'''
### 🔐 使用 Session 处理 Cookies 与登录

Session
能 ** 自动处理
Cookies **。服务器通过
Set - Cookie
头设置的
cookies
会被
Session
保存，并在后续请求中自动发送。

下面的例子演示了如何使用
Session
保持登录状态：


'''
```python
import requests

# 创建 Session
with requests.Session() as session:
    # 配置请求头
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    # 首先，访问登录页面获取令牌（如 authenticity_token）
    login_page_url = 'https://github.com/login'
    login_page_response = session.get(login_page_url)
    # 此处应解析登录页面获取必要的令牌，例如使用正则表达式
    # authenticity_token = ... (解析逻辑)

    # 准备登录数据
    login_data = {
        'login': 'your_username',
        'password': 'your_password',
        # 'authenticity_token': authenticity_token  # 需要从登录页面解析
    }

    # 提交登录请求
    login_url = 'https://github.com/session'
    login_response = session.post(login_url, data=login_data)

    # 登录成功后，使用同一个 Session 访问需要登录的页面
    profile_url = 'https://github.com/your_username'
    profile_response = session.get(profile_url)

    # 检查登录是否成功，例如检查响应内容或状态码
    print(profile_response.status_code)
    # 进一步处理响应内容...
```

'''

### 📋 Session 对象的主要方法

Session
对象提供了与
requests
模块顶层级函数类似的
HTTP
方法，如
`get()`, `post()`, `put()`, `delete()`, `head()`, `options()`, `patch()`。此外，还有一些其他有用的方法：

| 方法 | 主要作用 | 常用场景 / 说明 |
|:--- |: --- |:--- |
| `request()` | 发送请求的核心方法 | 其他便捷方法（如
`get`, `post`）内部调用它 |
| `get()`, `post()`
等 | 发送特定类型HTTP请求 | 与
`requests.get()`
等参数相同，但保持会话状态 |
| `close()` | 关闭会话，释放连接资源 | 对于长时间运行的程序，建议显式关闭 |
| `prepare_request()` | 预处理Request对象，返回PreparedRequest | 用于在发送前修改请求体或头 |

### 🔧 进阶用法与底层操作

1. ** 使用预备请求(PreparedRequest) **

这是
Requests
库中一个更底层的类，包含了将要发送到服务器的准确数据。通常从一个
Request
对象生成
PreparedRequest。使用
`Session.prepare_request()`
可以获取一个带有当前
Session
状态（如
cookies）的
PreparedRequest。

'''

```python
from requests import Request, Session

session = Session()
req = Request('GET', 'https://httpbin.org/get', headers={'x-test': 'true'})

prepped = session.prepare_request(req)

# 在发送前，可以修改预备请求的属性
# prepped.headers['x-test'] = 'modified'

resp = session.send(prepped)
print(resp.status_code)
```

'''

2. ** 确保资源释放 **

使用
Session
后，最好显式关闭它以释放资源。推荐使用
`
with` 语句上下文管理器，这样即使发生异常，Session 也会被正确关闭。


'''
# 推荐使用 with 语句
with requests.Session() as session:
    session.get('https://httpbin.org/get')
# 退出 with 块后，session 会自动关闭
''''
### ⚠️ 注意事项

- ** 方法层参数不跨请求保持 **：在单个请求方法（如
`get()`）中设置的参数（如
`cookies`）只对该次请求有效，不会保存在
Session
中并带到下一个请求。例如，第一个请求单独设置了
`cookies`
参数，下一个请求默认不会携带这个
cookie。
- ** 适配器配置 **：Session
使用适配器处理不同协议的连接细节。你可以通过
`get_adapter()`
方法获取适配器，或使用
`mount()`
方法为特定
URL
前缀挂载自定义适配器。

### 简单总结

`requests.Session`
是一个强大的工具，它通过 ** 连接复用 ** 和 ** 状态保持 ** 机制，极大地简化了需要处理多次请求、尤其是需要维持会话状态（如登录）的编程任务。
在编写需要与同一主机进行多次交互的程序时，使用Session通常是更高效和更专业的选择。

希望以上解析能帮助你更好地理解和使用`sessions`模块。如果你对特定方法或场景有更多疑问，我们可以继续探讨。

'''


import requests.sessions as RS

K=dir(RS)
for j in K:
    print(j)




    '''
    requests 库的 sessions 模块是其核心，主要提供了一个重要的 Session 类，用于在多个HTTP请求间保持参数和连接。
    下面是该模块的详细信息汇总，助你快速了解其结构。

模块组件	名称	                               主要功能/用途
类	    Session	                           提供会话上下文，跨请求保持参数（如cookies、headers）、连接池管理。
方法	    request(method, url, **kwargs)	   核心方法，构建并发送请求，其他便捷方法（如get, post）都调用它。
        get(url, **kwargs)	               发送GET请求。
        post(url, **kwargs)	               发送POST请求。
        put(url, **kwargs)	               发送PUT请求。
        delete(url, **kwargs)	           发送DELETE请求。
        head(url, **kwargs)	               发送HEAD请求。
        patch(url, **kwargs)	           发送PATCH请求。
        options(url, **kwargs)	           发送OPTIONS请求。
        prepare_request(request)	       预处理Request对象，返回PreparedRequest。
        send(request, **kwargs)	           发送PreparedRequest对象。
        close()	                           关闭会话，释放连接池等资源。
函数	    session()	                       返回一个新的Session对象。
    
    '''