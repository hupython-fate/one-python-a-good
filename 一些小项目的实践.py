com=['老王',
     '老宇',
     '老黄']
for name in com:
    comhhhh=name+'你好'+'。'
    print(comhhhh)

    '''
    一个能把列表里的名字替换给一个变量名的值的小程序。
    '''

#send_message(name,comhhhh)

cooo=['老王','老宇','老黑']
for nss in cooo:
    commmm='''你
    好，'''+nss+'''
    今年是好年'''
    print(commmm)

    #前一段字符串前加三引号，然后换行，可以跨行打印字符


    #format方法的尝试
x='酒'
y='醉'
ccchhh='''
       今朝有{0}今朝{1}，
       明朝无{0}不复还。
       谁人得知{1}前身，
       宛若倾城不欲还。
       '''.format(x,y)
#format方法用的是{}花括号。而不是[]方括号，也不是（）圆括号。
print(ccchhh)
