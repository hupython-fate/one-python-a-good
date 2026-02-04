kkk=1/3
def bai():
    print("这是用python重写的百钱买百鸡的程序")
    for x in range(0,101):
        for y in range(0,101):
            for z in range(0,101):
                if x+y+z==100 and x*5+y*3+z*kkk==100:
                    print(f"公鸡有{x}只，母鸡有{y}只，小鸡有{z}只!")
bai()

'''根据deepseek的说法，百钱买百鸡的正确解只有四种，而不是七种，也就是说这个python程序没有错误，错误的是c程序，因为小鸡的个数必须为3的倍数'''