import sys#这个库是用来干什么的？疑惑。
'''sys是python自带的标准库，在游戏中的用途通常用于退出程序，如sys.exit()，当用户点击窗口时，调用sys.exit()退出游戏。'''
import pygame

class OneOK:
    '''管理游戏资源和行为的类'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()#pygame库中的一个名为init()的方法。  #这是什么意思？用来初始化背景的。
        self.scc=pygame.display.set_mode((1200,800))#一个属性，pygame是库名，display是模块名？set_mode无疑是一个方法名，但是作用是什么？
        '''pygame.display是显示模块，set_mode()是创建游戏窗口的方法，（1200，800）窗口尺寸（宽*高）。
           返回一个Surface对象，代表游戏窗口。
        '''
        pygame.display.set_caption('胡成健的外星人入侵。')

    def run_game(self):
        '''定义一个名为run_game的方法，
        开始游戏主循环。
        '''
        while True:#一个while循环，因为条件为True,所以会无限循环下去。
            #侦听键盘和鼠标事件。嗯，如何实现的？
            for e in pygame.event.get():
                '''思考，pygame.event模块是什么功能的？get()方法又有什么作用？
                还有，我把书中的event改为了e,嗯，本质上，叫什么名字都可以。
                也就是说，pygame.event.get()返回的是一个列表（list)或字典(dict)？反正返回的必须是一个可迭代对象。
                书上说返回的是列表。
                '''
                if e.type == pygame.QUIT:
                    #嗯，这句话我看得懂，意思是，如果e的类型等于pygame.QUIT,可是，pygame.QUIT是什么类型？
                    sys.exit()#这个是用来关闭游戏，退出程序的方法。
            # 让最近绘制的屏幕
            # 已知pygame.display是显示模块，哪么flip()是什么方法?有什么用？
            # flip（）的作用是更新整个屏幕。
            #还有，不能隔多行注释。
            pygame.display.flip()
'''好家伙，定义一个方法，把流程控制里的三大要点集全了，while,for,if。'''

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ss=OneOK()#等号左边的是任意的变量名，右边的是类名。
    ss.run_game()#ss代表的是类名，run_game()是自定义的方法，是游戏的主循环。
    '''
    也就是说创建一个对象吗？
    还有，if __name__ == '__main__':是什么意思？
    嗯，我知道这个是一个布尔表达式，结果要么是True,要么是false.当结果为True时，执行if语句下面的内容。
    可是呢，我并没有定义某个变量为__name__啊？还有，'__main__'是什么意思？
    嗯，也就是说，__name__是一个变量名，而这个变量名有多个值？这些值还是str?
    
    '''
    '''
    嗯，解答，__name__是内置变量，当一个python文件被直接运行时，__name__的值会被自动设为'__main__'。
    当一个python文件被导入到其它文件时，__name__的值的文件名是文件名（不含.py后缀）
    '''