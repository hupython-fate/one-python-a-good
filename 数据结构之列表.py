from statistics import median

x=['hu','cheng']
x.append("jian")#这是方法，和函数有类似但有不同。意思是添加，append方法名。
#对象.方法名（内容）。这是方法的调用方式，
#函数名（对象）。这是函数的调用方式。
x.remove("jian")#意思是减去，remove方法名。
print(x)
'''
列表是可变的，append方法直接改变了列表，往列表理添加了新的元素。而remove则减少了列表内新的元素。
'''
y="holle worad"
print(y.upper())#这个方法名是upper，功能是把对象转化为大写。
print(y)#数据类型是不可变的，upper方法并没有改变字符串。
y=y.upper()#只有新赋值给y，才能把y改变。
print(y)
'''
数据类型是不可变的，而数据结构是可变的？错！元组不可变，元组是数据结构。
int,str,float,bool.None。。。。。。这些数据类型明确是不可变的。
列表是可变的，
'''

'''
python的列表可以放不同类型的数据，这一点与许多其它语言不同。
'''

z=['hu']
z.append(666)
z.append(3.33)
z.append(True)
z.append(None)
print(z)

'''
列表和字符串一样，都可以用len函数求长度。
'''
print(len(x))
print(len(y))
print(len(z))

#列表同样可以用索引提取出特定的字符。
#列表同样是从0开始数的。最后一个元素的索引为列表长度减一。
#len函数和索引[]是一对的。

print(y[10])
print(z[4])
print(x[1])
print(x[0])

'''
如果想要修改列表内的某一个元素，可以同过索引赋值。
'''

g=['我','shi','yi','ge','suai','ge']
print(g)
g[4]='mei'
g[5]='nv'
print(g)
#这样直接修改了列表内的某个值。


'''
python还有许多针对列表的内置函数。
'''
k=[-1,6,963,0.1,22222.369]
print(max(k))#求列表内的最大值。
print(min(k))#求列表内的最小值。
print(sorted(k))#会返回排序好的列表。