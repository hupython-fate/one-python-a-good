'''
逻辑运算符有三个，在python当中，
分别是安and,or,not.
逻辑运算符对python代码的运行有这非常重要的作用。
'''


#除了逻辑运算符，还有算数运算符和比较运算符两种操作符。
x=int(input("请输入你的x："))
y=int(input("请输入你的y："))
if x>30and y>60:
    print("我是一个人")
elif x<30or y<60:
    print('我是非人。')
elif not x==30:
    print('谁？')