Ren=['蛋白质','葡萄糖','油脂','水','无机盐或矿物质','维生素']
#用append()方法来追加列表内的元素，而不改变其它元素。
Ren.append('膳食纤维')
#可以打印出来看看结果。
print(Ren)
'''
append()方法可以让python的列表玩出更多的新花样。
如下：
'''
wu_yi_yi=[]#一个无意义的空列表。
try:
    wu_yi_yi.append('eat','sleep','')
except TypeError:
    print('这是错误示范，因为括号内只能添入一个元素。')

wu_yi_yi.append('性与爱情')
print(wu_yi_yi)#打印出来以查看是否添加成功。

'''

'''

