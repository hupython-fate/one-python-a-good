import requests
mou=dir(requests)# 方法1：使用dir()函数查看所有属性和方法
# 这会显示requests模块的所有公共接口
for k in mou:
    print(k)
help(requests)

#我现在还远远没有掌握和挖掘完requests这个工具的全部功能，先从api模块开始，一个模块一个模块的掌握和挖掘。

'''
学习路线建议
第一阶段：核心模块（建议按此顺序）
1. models 模块 ⭐⭐⭐⭐⭐
这是requests库的核心基础，包含最重要的类：

Request - 请求对象

PreparedRequest - 预备请求对象

Response - 响应对象

学习方法：


dir() 函数返回一个对象的所有属性和方法的名称列表。

python
from requests import models
# 查看所有属性和方法
print(dir(models))

# 重点研究这几个类的构造方法和属性
req = models.Request()
print(dir(req))

resp = models.Response()
print(dir(resp))





2. sessions 模块 ⭐⭐⭐⭐⭐
包含Session类的实现，是保持跨请求参数的关键：

Session - 会话类

连接池管理

Cookie持久化

3. api 模块 ⭐⭐⭐⭐
包含你日常使用最多的便捷函数：

request() - 核心请求函数

get(), post(), put(), delete()等

第二阶段：功能模块
4. adapters 模块 ⭐⭐⭐⭐
HTTP传输适配器，处理底层连接：

HTTPAdapter - HTTP适配器

连接池配置

5. auth 模块 ⭐⭐⭐
认证处理：

HTTPBasicAuth - 基本认证

HTTPDigestAuth - 摘要认证

6. cookies 模块 ⭐⭐⭐
Cookie管理：

RequestsCookieJar - Cookie容器

第三阶段：工具和辅助模块
7. utils 模块 ⭐⭐⭐
各种工具函数

8. exceptions 模块 ⭐⭐
异常类定义

9. structures 模块 ⭐⭐
数据结构，如CaseInsensitiveDict

'''