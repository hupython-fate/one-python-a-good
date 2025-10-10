import requests

# 创建会话
session = requests.Session()

# 登录数据
login_data = {
    'username': 'your_username',
    'password': 'your_password'
}

# 发送登录请求
login_url = "https://example.com/login"
response = session.post(login_url, data=login_data)

# 检查登录是否成功
if response.status_code == 200:
    # 访问VIP内容
    vip_url = "https://example.com/vip-content"
    vip_response = session.get(vip_url)

    # 解析vip_response.content
else:
    print("登录失败")



    '''
    Cookie 的中文意思
Cookie 的中文翻译是：
"小型文本文件" 或 "网站数据缓存"

更通俗的理解：
网站记忆卡 - 网站用来记住你的小卡片

身份标签 - 网站给你贴的识别标签

浏览足迹 - 记录你在网站上的行为痕迹

Session 的中文意思
Session 的中文翻译是：
"会话" 或 "对话期间"

更通俗的理解：
网站对话 - 你与网站的一次完整交流过程

登录会话 - 从登录到退出的整个期间

临时工作区 - 服务器为你分配的临时工作空间

详细对比解释
Cookie（小型文本文件）
工作原理：

python
# 就像你去咖啡店，店员给你一张积分卡
# 每次你去的时候，出示这张卡，店员就知道你是谁

# 在技术上的体现：
# 服务器 -> 浏览器：给你一个Cookie（Set-Cookie头）
# 浏览器 -> 服务器：每次请求都带上这个Cookie（Cookie头）
实际例子：

python
# 当你登录网站时
服务器说："好的，你登录成功了，这是你的身份卡（Cookie），有效期7天"
浏览器："好的，我会保存这张卡"

# 后续访问时
浏览器："嗨，我又来了，这是我的身份卡（Cookie）"
服务器："哦，是你啊，欢迎回来！"
Session（会话）
工作原理：

python
# 就像你去银行办理业务
# 银行给你一个号码牌（Session ID），你的所有资料都在柜台里面

# 在技术上的体现：
# 服务器创建会话 -> 生成Session ID -> 通过Cookie传给浏览器
# 服务器端存储会话数据 -> 通过Session ID查找对应数据
实际例子：

python
# 登录过程
用户："我要登录"
服务器："好的，我给你创建了一个工作空间（Session），这是进入的钥匙（Session ID）"

# 购物过程
用户："把这个商品加入购物车"
服务器："好的，我已经在你的工作空间（Session）里记下来了"

用户："查看购物车"
服务器："让我看看你的工作空间（Session），哦，你有这些商品..."
技术层面的详细区别
特性	Cookie	Session
存储位置	客户端浏览器	服务器端
数据安全	较低（用户可见）	较高（服务器控制）
存储容量	较小（4KB左右）	较大（受服务器限制）
生命周期	可设置过期时间	通常到浏览器关闭
性能影响	每次请求自动发送	需要服务器查找
在爬虫中的具体应用
Cookie 在爬虫中的使用
python
import requests

# 模拟登录后获取


    
    '''