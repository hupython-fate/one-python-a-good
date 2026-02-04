n='HHHHHHH'
print(n.title())

print(n.upper())#全大写的转化方法。

print(n.lower())#全转化小写的方法。


g='hu'
l='ceng'
llk=f'{g} {l}'
print(llk)
#将花括号内的变量名替换成对应的值。
#这种字符串被称为f字符串。
#f里套f的做法。
print(f'holle, {llk.title()}!')#llk是变量名，也是title这个方法的操作对象。

jjjjj=f'holle, {g.title()} {l.title()}!'
print(jjjjj)

print('''








000''')

#使用制表符或换行符来添加空白。

print('python')
print('\tpython')#\t应该叫制表符。

print('my name is\nhu cheng jian\nwhy?\nbecomse this my parent')#\n应该叫换行符。

#制表符和换行符可以同时使用。
print('my firend have:\n\tli ming\n\tli hua\n\tliu hua')#这是一个例子。


#删除字符串里的空白。
kkkkkk='my nee        '
print(kkkkkk.rstrip())#这个方法rstrip()可以把右端的空白删除。
print(kkkkkk)#暂时删除的空白。


#永久删除空白。
kkkkkk=kkkkkk.rstrip()#对这个变量重新赋值。
print(kkkkkk)

#删除左边的空白，如下：
yi_ge_h='   左右都有空格    '
yi=yi_ge_h.lstrip()#删除左边的空格
er=yi_ge_h.rstrip()#删除右边的空格
san=yi_ge_h.strip()#删除左右两边的空格

print(yi)
print(er)
print(san)



#字符串操作之删除前缀
sbb='ssssssss:123456789'
f=sbb.removeprefix('ssssssss:')#removeprefix()方法可以把某个字符串内的前缀删除。
print(f)
#ggg=sbb.removeprefix('123456789')
#print(ggg)
#只能用来删除前缀，后面的删除不了。
#如果想要永久删除某个前缀，那么可以赋值。
sbb=sbb.removeprefix('ssssssss:')
print(sbb)


