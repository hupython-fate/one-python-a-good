from selenium import webdriver
from selenium.webdriver.edge.options import Options
'''selenium.webdriver.edge：这是webdriver包中专门用于Edge浏览器的子包

options：这是edge子包中的一个模块

Options：这是options模块中的一个类，用于配置浏览器选项'''



options = Options()
options.add_argument('--headless')#option是上一行创建的对象，add_argument()是依附于这个对象的方法。
'''Options()：创建Options类的实例（一个具体对象）

add_argument()：Options实例的方法，用于添加命令行参数

--headless：参数值，让浏览器在后台运行（不显示界面）'''




driver = webdriver.Edge(options=options)#这是在创建一个实例对象。
'''webdriver.Edge：这是webdriver包中的一个类

Edge()：创建Edge类的实例（一个具体的浏览器控制对象）'''





url='https://movie.douban.com/chart'#一个用来储存url的变量
driver.get(url)
print(driver.page_source)# 调用driver实例的page_source属性，获取页面HTML源码
#对象名.属性   经典的获取对象的属性的操作，明明在林莉莉的网课上已经学过，但是看到这个还是没认出来，没理解到位，真是经验不足啊。要多加练习啊，
#在ai给出的大量代码示例中，锻练自己的代码分析和识别能力。



'''成功了，我成功了！我终于获取到了经过动态渲染后的html源代码，今天是2025年10月4日，是一个里程碑式的日子。
虽然这段代码还有一些不理解的，但是还是好开心，因为这意味着我的爬虫能力上了一个新台阶！
'''