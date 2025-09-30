def IMB():
    ti_zhong=57.7
    shen_gao=1.66
    IMB=ti_zhong/shen_gao**2
    print(IMB)
IMB()

#以上的函数缺乏参数。依旧会带来一些重复代码。

#新的更有用的代码是：
def KKKK(X,Y):
    KKKK=X/Y**2
    print(KKKK)
    '''
    这行代码中括号中的x和y，是参数。
    调用这个函数时，例如kkkk(222,666).这样调用函数时，括号里的内容相当于变量的值，而缩进的内容中x和y，则相当于变量名。
这和input函数类似，都可以用来获取用户输入的内容。
如果把input函数和if语句结合起来，则可以达成函数的一部分功能.
    '''
KKKK(57.7,1.66)#函数名有严格的大小写区分。如果定义的函数名是kkkk,但是调用函数时用的却是KKKK，那么就会报错。

'''
#return语句还没学会，为什么？
#然而，还有return语句，它会返回某个变量的值。
#比如：
'''

def llll(x,y):
    lll=x**2+y**2
    print(lll)
    return lll
#llll(2,2)
#print(llll)#这个用法是错误的，正确的做法是先把函数贴一个变量名，再打印这个变量名，才会打印出对应的值。
#print(lll)
llll(4,4)#不用额外的print，只需调用这个函数就可以输出。#这个函数输出的是32
#print(lll)
asdf=llll(4,4)#这样输出的是32
print(asdf)#这样输出的是空值None.
#在函数的末尾加了return语句，返回了我们想要的变量名时，输出的结果就不是None了，而是32.

#通过加return语句和“变量名1=自定义的函数名（参数，参数）”的形式，可以记录函数的值，使一个函数的值可以多次利用。
'''
缩进的变量是局部变量，无法被print获取，这是因为作用域不同。
然而，只要“return+变量名”，这个变量名就会被返回？
'''


def BMI_JI_SHUAN_QI(SHEN_gao,ti_zhong):
    BMI=ti_zhong/SHEN_gao**2
    if BMI>=24.0:
        print(f'您的BMI指数为{BMI},属于偏胖范围。')

    elif BMI<24.0 and BMI>19.0:
        print(f'您的BMI指数为{BMI}，属于正常范围。')

    else:
        print(f'您的BMI指数为{BMI}，属于偏瘦范围。')
    return BMI


#结合input语句可以做一个交互式的游戏了。