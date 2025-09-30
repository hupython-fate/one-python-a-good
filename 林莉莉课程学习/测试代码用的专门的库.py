import unittest as u
from test_a_one import my_add

#创建一个类，名字以Text开头，表示这是用来测试的类。
class TestAAAA(u.TestCase):
    #这个测试类下面，每一个方法都是一个测试用例。
    def Test_yi_ge_chang_shi(self):#每个测试用例的命名开头必须用Test_开头，这非常关键。
    #因为这个类只把Test开头的当作测试用例。
        self.assertEqual(my_add(5,5),7)#用self调用父类的方法。
    #然后，在终端中输入python -m unittest



'''
搞不懂，
为什么在终端输入python -m unittest会没有测试出问题。
而直接运行文件又会报出无法解决的报错。
感觉这个测试库很鸡肋。
'''
