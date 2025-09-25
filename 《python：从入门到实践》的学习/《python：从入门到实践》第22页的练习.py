'''
第一条练习：
'''
name='hu cheng jian'
f=f'ni hao {name} xi wan ni hao hao huo zhe.'
print(f)
#第一条练习完成

'''
第二条练习：调整名字的大小写
'''
name_1='hu cheng jian'
name_2=name_1.title()#把首字母大写。
name_3=name_1.upper()#把全部的字母大写。
name_4=name_3.lower()#把全部大写的字母全部转换成小写。
print(name_1)#原原本本的小写
print(name_2)#首字母大写
print(name_3)#全部字母大写
print(name_4)#全部字母小写

'''
第三条练习：把名人和他说过的名言打印出来
'''
mao_ze_dong="mao cen jing shuo guo:\"精神变物质，物质变精神。\""
print(mao_ze_dong)

'''
第四条练习：
'''

f_p='毛泽东'
wei_ren=mao_ze_dong.removeprefix('mao cen jing shuo guo:')#把前缀删掉
print(f'{f_p}说过：{wei_ren}')
'''
第五条练习：删除人名中的空白
'''
min_zi='    刘华    \n    李昌    \n\t这两个都是我的好朋友。     '
print(min_zi.rstrip())#删除右边的空白
print('''


''')
print(min_zi.lstrip())#删除左边的空白
print('''



''')
print(min_zi.strip())#删除左右两边的空白


'''
第六条练习：文件括展名
'''
fil='python_good.py'
ppp=fil.removesuffix('.py')#removesuffix()方法可以用来删除后缀。
print(ppp)