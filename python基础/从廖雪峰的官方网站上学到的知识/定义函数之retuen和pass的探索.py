def my_ads(x):
    pass
#一个空函数，如果你还没想好这个函数的内容，可以先写一个pass,来避免语法错误。

def my_ok(x,y):
    z=x+y
    return z
#我的习惯和错误认识是把return视为可有可无的西，并用print（）代替return.
def my_print(x):
    return x
def my_print2(x,y,z):
    c=x+y+z
#如果没有return的话，一个函数最后的值会是空值None。
#还有，return一般是放在函数的最后一行的。
#以后不要用print()来代替return了。
k=my_print2(1,2,3)
print(k)#输出的是None.