def ping_fang_he(x):
    z=x ** 2
    return z

def li_fang_he(x):
    z=x**3
    return z

def si_ci_fang(x):
    z=x**4
    return z

def jia_shi(x):
    z=x+10
    return z

def f(z):
    print(f'''
    |输入的数字运算后的结果|{z}|
        ''')

def gao_jie_han_shu(x,han_shu,ge_shi_hua):
    z=han_shu(x)
    ge_shi_hua(z)


gao_jie_han_shu(2,ping_fang_he,f)
gao_jie_han_shu(1,jia_shi,f)
#用一下匿名函数。

gao_jie_han_shu(2,lambda x:x+100,f)
#lambda+一个空格， 关键字后面加上参数名，然后接冒号“：”，冒号后面的是函数的内容，无需用return返回结果，因为它会直接返回。
#如果想给匿名函数增加参数，做法如下：
def ffff(x1,x2,han_shu):
    han_shu(x1,x2)
    print(han_shu(x1,x2))

ffff(2,3,lambda x1,x2:x1+x2)
ffff(2,3,lambda x1,x2:x1*x2)

r=(lambda x:x**2)(3)
print(r)

#匿名函数的局限性是它的冒号后面无法有多个语句，复用也不方便。