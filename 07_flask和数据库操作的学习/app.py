from flask import Flask
import config
from flask import request  #用于query String 传参
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


if __name__ == '__main__':
    app.run()
