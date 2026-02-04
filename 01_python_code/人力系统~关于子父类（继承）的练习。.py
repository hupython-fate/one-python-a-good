class YuanGong:
    def __init__(self,gong_hao,name):
        self.g=gong_hao
        self.name=name

    def print_fo(self):
        print(f'此员工的姓名为{self.name}，员工编号为{self.g}。')

class Quan(YuanGong):
    def __init__(self,gong_hao,name,yue_xing):
        super().__init__(gong_hao,name)#继承父类不用在括号里加self.否则会报错。
        self.yue=yue_xing

    def print_Q(self):
        return self.yue



class Jian(YuanGong):
    def __init__(self,gong_hao,name,ri_gong_zhi,gong_zuo_tian_su):
        super().__init__(gong_hao,name)
        self.r=ri_gong_zhi
        self.gg=gong_zuo_tian_su

    def print_J(self):
        return self.r * self.gg#这里创建对象时要注意不能填入字符串。


    '''
    好开心啊！写代码真快乐，人生中第一个简单的人力系统。我充满了成就感。
    虽然是跟着林莉莉的视频写的，但还是好开心。
    '''


    #创建一个对象实验一下。


zeng=Jian('123456','曾杰',100,7)

kkkk=zeng.print_J()#对象名+“.”+“自定义的方法名”，即可打印出这个员工的工资。
llll=zeng.print_fo()#这个可以打印出员工的姓名和id.
print(f'{zeng.name}的工资为{kkkk}')


li=Quan('222222','老李',5000)
hhhh=li.print_Q()
ASDF=li.print_fo()
print(f'{li.name}的月工资为{hhhh}')