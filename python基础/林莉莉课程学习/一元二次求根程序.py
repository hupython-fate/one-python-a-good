import math
import cmath

def yi_yuan_er_ci_qiu_gen(a,b,c):
    #bei_ta大于零时。
    bei_ta=b**2-4*a*c
    if bei_ta>0:
        print('此一元二次方程有两个根：')
        print('第一个根的值为：'+str((-b+math.sqrt(bei_ta))/(2*a)))#可以用math库里的sqrt函数。sqrt（x），会返回x的根号值。
        print('第二个根的值为：'+str((-b-(bei_ta)*(1/2**2))/(2*a)))#根号也可以写成（1/2**2）的形式。
    elif bei_ta==0:
        print('此一元二次方程有一个根：')
        print('根的值为：'+str(-(b/2*a)))
    else:
        print('此一元二次方程无实数根。')
        print('但在复数范围内，有两个共厄复数根：')
        #print('第一个共厄复数根的值为：'+float(-(b/2*a)+(-b-(bei_ta)*(1/2**2))/(2*a)j))


a=float(input('请输入a的值：'))
b=float(input('请输入b的值：'))
c=float(input('请输入c的值：'))
yi_yuan_er_ci_qiu_gen(a,b,c)
