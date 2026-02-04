'''

简易计算器
功能：实现加、减、乘、除基本运算
涉及语法：变量、函数、条件语句、输入输出
正反馈：立即看到计算结果是否正确

'''



#x=input('请输入一个数字：')
def jia(x,beijiasu):
    y=x+beijiasu
    print(y)

def jian(jiansu,beijiansu):
    z=jiansu-beijiansu
    print(z)

def ceng(cengsu,beicengsu):
    g=cengsu*beicengsu
    print(g)

def chu(chusu,beichusu):
    h=chusu/beichusu
    print(h)

#jia(2,6,)

#以上这个程序的问题是，一，只能计算两项式，二，没有用户输入，三，无法实现用户输入一个算式，点一下回车就计算出结果的效果。

#如果曾加参数的话，那么也不知道要曾加多少参数。

#这个是不行的。

y=int(input(f'请输入算式（例如1+2+3==6):{}'))
#获取用户的算式。
print(y)#打印出来的是字符串。
#二是计算出结果。

print("三是打印出计算结果，让用户知道。")#这可以用一个变量来获取计算结果。