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

如果把input函数和if语句结合起来，则可以达成函数的一部分功能。


    '''


KKKK(57.7,1.66)#函数名有严格的大小写区分。如果定义的函数名是kkkk,但是调用函数时用的却是KKKK，那么就会报错。


#然而，还有return语句，它会返回某个变量的值。

#比如：
#return语句还没学会，为什么？
def llll(x,y):
    llll=x**2+y**2
    print(llll)
    return llll

llll(2,2)
print(llll)