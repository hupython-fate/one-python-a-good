import requests.models as models
import requests.sessions as sessions


# 1. 创建请求对象 (models模块)
request = models.Request()
request.url = 'https://api.example.com/data'
request.params = {'page': 1}  # 请求特定参数

session=sessions.Session()
# 2. 准备请求 (sessions模块介入)
#prepped = req.prepare()#工产方法，返回PreparedRequest实例。用models模块中的也可以。
prepared_request = session.prepare_request(request)
#把创建的request对象转化为PrepareRequest对象。
# 此时会合并session级别的默认params和request级别的具体params

# 3. 发送请求 (sessions模块)
response = session.send(prepared_request)