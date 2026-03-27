from flask import Flask
import config
from flask import request  #用于query String 传参
from flask import url_for,redirect
from flask import render_template
app = Flask(__name__)

app.config.from_object(config)

@app.route('/')#url部分
#@符号在python中是用作装饰器的。
def hello_world(): # put application's code here
    #视图函数
    return 'Hello Worqqwe!'
#当用户去访问这个url的时候，程序就会执行这个视图函数。

@app.route('/pre')
def pre():
    return '这是一个视图函数！'

#1,定义path传参
@app.route('/blog/<id>')
def blog(id):
    return f'您访问的用户id为：{id}'

#上面的blog是在定义一种有参url,id是参数，如果不加其他东西的话，那么id默认就是字符串。
#当然，还可以使用数据类型进行限定，
#比如，

@app.route('/bd/<int:asd>')
def shui_yi(asd):
    return f'号码为：{asd}'


#2.query String传参
@app.route('/qwe')
def shiyang():
    #解释一下，这句话的意思是，传递名为cheng_shu_name,如果没有创递这个参数，默认值为1,类型规定为int。
    kkk=request.args.get('chang_shu_name',1,type=int)
    return f'获取到的参数为{kkk}'
#在浏览器中，就可以通过/qwe?chang_shu_name=123来访问这个视图，如果有多个参数，那么就可以用&符号连接。

#比如说
@app.route('/eee')
def eee():
    n1=request.args.get('qwer')
    n2=request.args.get('qer')
    return f'{n1}+{n2}'


@app.route('/blogg/add',methods=["POST","GET"])
def blog_add():
    return "博客添加成功。"


#还可以使用快捷路由，并不一定要一直使用route。
@app.get('/l')  #这个装饰器相当于@app.route('/l',methods=["GET"])
def l():
    return 'l'

@app.post('/ll')  #相当于 @app.route('/ll',methods=["GET"])
def ll():
    return 'll'

'''
浏览器只能用get请求。
'''

#接下来学习页面的重定向

'''在flask中，重定向是通过flask.redirect(location,code=302)这个函数来实现的。302代表暂时重定向，301代表永久重定向'''

@app.route("/a")
def a():
    name=request.args.get('name')
    if not name:
        return redirect("/eee")
    else:
        return name

#下面开始教受jinjia2的模板加载引擎。

@app.route('/b')
def kkk():
    return render_template('index.html')


#以下是使用动态变量的示例

class user:
    def __init__(self,name,dianhua):
        self.name=name
        self.dianhua=dianhua

        '''学习过了java，回过头来学习和使用python，对类和对象的使用和理解更加的深刻了啊
        
        现在看这个构造方法，就能看出，self就相当于this，除了self，这就相当于java中的有参构造方法，但是
        非静态成员变量只需要在self.成员变量名，这种太太简便的代码，写起来一时有些不习惯啊。
        '''
@app.route('/d')
def aaa():
    hhh='adadsfasdfa00'
    ppp2={
        "name":"李俊",
        "age":23
    }
    sss=user("张三","0000987234")
    ##现在只有三个参数，这还好，当有更多的参数时，是不是要用更多的形参？
    #答案是不用，这只是第一种形式，实际上还有一种形式。
    #return render_template('kkk.html',hhh=hhh,ppp=ppp2,s=sss)

    con ={
        "hhh":hhh,
        "ppp":ppp2,
        "s":sss
    }
    return render_template('kkk.html',**con)

    #以上是第二种形式，用一个字典，把所有的参数放进去，然后用**字典名的方式进行传参。


if __name__ == '__main__':
    app.run()
