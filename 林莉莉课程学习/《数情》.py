'''
只需要懂得输入（input）和输出（print),还有变量和条件判断（if、elif、else），再加上不断的俄罗斯套娃，就可以开发一款普通的小游戏了。

当然，如果想要进阶，还要懂得GUI的制做。

有没有办法让函数的知识参与呢？试试。

python是纯面象对象编程，也许我可以首先创建一个类，即游戏主角和攻略对象的的模板，然后，用这个模板创建李静、邓欣、小美三个对象，还有主角。

还有对象的方法，如果是恋爱游戏，那么对象能做的事有什么？

约会、逛街、谈话、

但是，循环、错误处理、文件处理、列表、字典、元组、集合、和各种操作符、测试等知识都完全没有用到。

'''

#一次尝试：
class RenWu:
    def __init__(self,fair,yan_jing_se,xing_ge,xing_bie,shen_gao,ti_zhong,name,job):
        self.f=fair
        self.s=yan_jing_se
        self.xing=xing_ge
        self.xin=xing_bie
        self.sheng=shen_gao
        self.ti=ti_zhong
        self.name=name
        self.job=job

    def eat(self,where,time,ren,what):
        print(f'和{ren}在{time}时，于{where}吃{what}。')

    def sleep(self,where,time,ren):
         print(f'和{ren}在{where}，于{time}时睡觉。')

    def guan_jie(self,where,time,ren):
        print(f'和{ren}在{where}，于{time}逛街。')

    def xue_xi(self,where,time,ren,what):
        print(f'和{ren}在{where}，于{time}学习{what}')

    def you_xi(self,where,time,ren,what):
        print(f'和{ren}在{where}，于{time}时打{what}游戏。')

    def den_san(self,where,time,ren,what):
        print(f'和{ren}在{where}，于{time}时登{what}山。')




xiao_mei=RenWu('黑色双马尾','黑色','幽默风趣，非常可爱','女','身高1.62','体重50kg','小美','学生')
li_jing=RenWu('黑色长发','棕黑色','文静，好奇心重',"女",'身高1.80','体重43kg','李静','学生')
den_xin=RenWu('黑色短发齐耳','棕色','霸气，笑起来相当好看','女','身高1.70','体重47.0kg','邓欣','学生')
zu_jue=RenWu('黑色碎发','棕黑色','温柔，喜欢写代码','男','180','60.0','叶凡','学生')





xiao_mei.eat('和平大饭店','上午9点钟','李静','蛋炒饭')



class building:
    def __init__(self,lou_chen,gao_du,name,zhi_min_du,jing_ji_shui_ping):
        self.lou=lou_chen
        self.gao=gao_du
        self.name=name
        self.zhi=zhi_min_du
        self.jing=jing_ji_shui_ping

    def you_hui(self,tiao_jian,da_ze_shu):
        if tiao_jian==True:
            print(f'今日打{da_ze_shu}折。')


ping_an_da_jiu_dian=building('3层',"10m",'平安大酒店','平平无奇小酒店',"10线小城市")




#类和对象已经创建好了，那么如何实现‘给用户三个选项，让用户自由选择其中一个，随后又冒出新的选项给用户选择，循环往复，至到游戏通关或失败”的效果呢？

#如果是选项，也许可以用字典。



#print('''如果有一份真挚的爱情摆在你的面前，你的选择是？
    
#'前情提要：你是一个高中生，学习成绩中等偏下，但是长相帅气，很受女生的欢迎。有三个女生非你不可，她们的名字分别是李静、邓欣、小美。

#'a,小美：不戴眼镜，有刘海，黑色长发头发，黑色瞳孔，身高1.62，体重50kg,性格幽默风趣，非常可爱。

#'b,邓欣：戴黑框眼镜，有一点刘海，黑色短发齐耳，棕色瞳孔，身高1.70，体重47.0kg,喜欢穿红色的外套，性格霸气，笑起来相当好看，当班干部，运动能力非常好，相当有魅力。

#'c,李静：刘海齐眉，有时会戴黑框眼镜，但平是不戴，黑色秀发，性格文静，好奇心重，棕黑色瞳孔，大眼睛，喜欢看书，班上的普通学员，身高和你一样，体重43kg,身高1.80。

#'d,都不选，女人算什么？有学习香吗？

#''')

xuan_ze={}
xuan_ze['a']='''\"小美，我喜欢你，请你和我在一起吧！\"
    
    小美犹豫了一下，回道：“xxx,你是个好人，但是我们不适合，你还是找别人吧。”  
    
    此时，你有三个选择，
    a,你神色坚定的回道：“小美，我不会放弃的，我一定会娶你的。”
    b,你神色暗然，回道：“好吧，对不起，小美，打扰了。”
    c,你  '''

xuan_ze['b']='邓欣：戴黑框眼镜，有一点刘海，黑色短发齐耳，棕色瞳孔，身高1.70，体重47.0kg,喜欢穿红色的外套，性格霸气，笑起来相当好看，当班干部，运动能力非常好，相当有魅力。'
xuan_ze['c']='李静：刘海齐眉，有时会戴黑框眼镜，但平是不戴，黑色秀发，性格文静，好奇心重，棕黑色瞳孔，大眼睛，喜欢看书，班上的普通学员，身高和你一样，体重43kg,身高1.80。'
xuan_ze['d']='都不选，女人算什么？有学习香吗？'

#也许可以这样。
#先print出abcd四个选项的内容，然后创建一个字典，然后，abcd四个键对应的是选这键后的内容。
'''
print('''
请作出一个选择：
a,这个选项的内容。比如，小美。
b,这个选项的内容。比如，小明。
c,这个选项的内容。比如，小黑。
d,这个选项的内容。比如，小帅。
''')
#在创建一个选择了这个选项之后对应内容的字典。
kkk={}
kkk['a']='选择a后，新的三个选项，和内容。'
kkk['b']='选择b后，新的三个选项，和内容。'
kkk['c']='选择c后，新的三个选项，和内容。'
kkk['d']='选择d后，新的三个选项，和内容。'
#再用input，获取用户的输入。
x=input('请输入你的选择：')
#然后再结合if判断和打印对应的键的值。
if x=='a':
    print(kkk[a])
    y=input('请输入你的第二次选择：')
    if y=='a'~~~~~~~~~~~~~~~~~~~~~~
elif x=='b':
    print(kkk[b])
elif x=='c':
    print(kkk[c])
else x=='d':
    print(kkk[d])
'''
#但是，还有很大的问题，因为这样写就要创建相当多的字典了，
#而且，还是免不了一座if山的堆砌。
#有什么方法可以避免if山的堆砌吗？
#比如说，操作符中的逻辑运算符？
#还是说，函数?可是，如何定义函数才可以代替if山的堆砌？




xuan_ze=input('起输入你的选择：')
if xuan_ze=='a':
    print('''
    
    ''')

elif xuan_ze=='b':
    print('')
elif xuan_ze=='c':
    print('')
elif xuan_ze=='d':
    print()
else:
    print('出错了，请输入可选的数据，还有可能是数字的大小写出错了，请结束程序后重新输入。')

