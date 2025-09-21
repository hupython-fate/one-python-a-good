class RenLei:
    def __init__(self,name,age,Xing_Bie,FaSe,xing_ge,sheng_gao,ti_zhong,xie_xin,chu_shen_shi_jian):#这个__init__()构造函数是用来定义对象拥有的属性的模板。但还有构造方法的。
        self.n=name#等号左边的可以是任意字符（变量名），等号右边的是要创建的类（class)的属性名,属性名必须与构造函数括号内的属性名一一对应。
        self.a=age
        self.x=Xing_Bie
        self.F=FaSe
        self.sb=xing_ge
        self.sh=sheng_gao
        self.ti=ti_zhong
        self.xie=xie_xin
        self.shen=chu_shen_shi_jian

    def eat(self,nei,where):
        print(f'{self.n}在{where}里吃{nei}.')

    def sleep(self,where):
        print(f'{self.n}在{where}睡觉。')



#以下是以这个类为模板创建的一个对象。
RenLei_1=RenLei('huchengjian',18,'nang','hei')#括号内添入实例对象的具体数值，属性名相当于变量名，填入具体数值相当于为这个变量名赋值。
print(RenLei_1.n)#n即代表属性名。#RenLei_1则是创建的对象名。
#运行上述代码将会得到这个对象（RenLei_1）的某个属性（name)对应的值。
'''
类是对象们的模板，对象们是类的实例。
类就像事物们的共性归纳，而对象，每个对象都是不同的个性。

'''
print(f'这个人的名字是{RenLei_1.n},{RenLei_1.n}的年龄是{RenLei_1.a}岁，性别是{RenLei_1.x},发色是{RenLei_1.F}.')


#创建第二个对象

RenLei_2=RenLei('liu hua',40,'nang','hei')

#用这个新创建的对象来执行动作。
RenLei_2.eat('do jian','shi tan')#有多少个参数就要填入几个。
#对象名+点+自定义的方法名+括号（），括号内填入参数。不用特意加print，就可以调用这个对象去做一些事情。

