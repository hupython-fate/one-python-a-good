#BMI等于体重/身高**2，身高的单位是米，体重的单位是kg。

x=float(input('请输入你的体重(单位是kg）；'))
y=float(input('请输入你的身高（单位是m）；'))
BMI=x/y**2
print('您的BMI指数为'+str(BMI))

input('请输入任意符号后结束程序运行：')