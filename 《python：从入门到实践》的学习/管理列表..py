'''
使用sort()方法对列表进行永久排序。
注：这个排序是永久的修改。
按字母的顺序。
'''

name=['aii','jii','kee','giiii','shi1kh','weo','dddd','ii']
name.sort()
print(name)

#也可以反方向进行排序。
name.sort(reverse=True)
print(name)

print('   ')

'''
也可以用sorted()函数对列表进行临时排序。
'''
print('以下是原始数据：')
print(name)#先打印原始数据。
print('以下是临时更改的列表数据（按字母顺序)：')
x=sorted(name)
print(x)#打印临时更改的列表顺序。
print('再次打印这个列表（list),就会发现列表的实际顺序并没有变：')
print(name)#再打印这个列表，就会发现列表的顺序并没有变。


'''
反向打印列表：reverse()方法反向打印列表，这种修改是永久的。
'''

name.reverse()
print(name)
#注意，反向打印的列表不是按字母顺序反向的，而是直接反向。