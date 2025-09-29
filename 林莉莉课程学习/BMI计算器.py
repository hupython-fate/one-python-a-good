#BMI等于体重/身高**2，身高的单位是米，体重的单位是kg。
#x=float(input('请输入你的体重(单位是kg）；'))
#y=float(input('请输入你的身高（单位是m）；'))

def BIM(x,y):
    bim=x/y**2#函数中的变量应小写。
    print('您的BMI指数为'+str(bim))
    return bim

y=float(input('请输入你的身高（单位是m）；'))
x=float(input('请输入你的体重(单位是kg）；'))
bim_1=BIM(x,y)

print(bim_1)

input('请输入任意符号后结束程序运行：')
#使用函数改进了这个程序，保留了获取用户输入的功能，使用了变量和函数。

