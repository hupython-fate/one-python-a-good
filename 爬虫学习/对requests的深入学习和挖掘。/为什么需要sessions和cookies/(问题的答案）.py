''' 会话状态管理
为什么需要 Session？
由于 HTTP 是无状态的，需要机制来保持"会话"：

python
# 没有 Session - 每次都是新对话
requests.get(url)  # "你好，我是用户A"
requests.get(url)  # "你好，我是谁？"

# 有 Session - 保持对话状态
session = requests.Session()
session.get(url)   # "你好，我是用户A"
session.get(url)   # "你好用户A，我记得你"




Cookies 的作用
Cookies 是服务器发给客户端的一小段数据，客户端在后续请求中自动送回：

python
# 登录后服务器设置 cookie
response = session.post(login_url, data=credentials)
# session 自动保存 cookie

# 后续请求自动携带 cookie
profile = session.get(profile_url)  # 保持登录状态

'''