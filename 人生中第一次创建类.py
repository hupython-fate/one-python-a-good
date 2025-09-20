class RenLei:
    def __init__(self,name,age,XingBie,FaSe):#这个__init__()构造函数是用来定义对象拥有的属性的模板。但还有构造方法的。
        self.n=name#等号左边的可以是任意字符（变量名），等号右边的是要创建的类（class)的属性名,属性名必须与构造函数括号内的属性名一一对应。
        self.a=age
        self.x=XingBie
        self.F=FaSe

    def eat(self,he,jiao,yan):
        self.h=he#必须要把属性名赋值给某个变量。
        self.j=jiao
        self.y=yan



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
RenLei_2.eat