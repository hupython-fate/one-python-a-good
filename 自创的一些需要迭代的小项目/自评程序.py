#这是一个自评程序，嗯，算法是通用的。
import os
h='自评文件集'
if not os.path.exists(h):
    os.makedirs(h)
def zi_ping():
    cc=input("如果你是想要写今日的自我评价，请输入a,如果你是想要查询某一天的自评，请输入b:")
    if(cc=='a' or cc=='A'):
        a=input("请输入今天的自我评价：")
        b=input("请输入今日的日期（请务必用“xxxx年，xx月，xx日。”的格式输入）：")
        filename="./自评文件集/"+b+".txt"
        with open(filename,"w",encoding='utf-8') as f:#a是赋加模式。
            f.write(a)
        c=input("请问你是要再次输入自评，还是要查询某一天的自评呢？如果是前者，请输入1，如果是后者，请输入2：")
        if c=='1':
             aa=input(f"请再次输入自评，这次的自评会放到{filename}这个文件中：")
             with open(filename,"a") as k:
                 k.write(aa)
        elif c=='2':
            bb=input(f"请输入你想要查询的日期，务必请以“xxxx年，xx月，xx日。”的格式查询！：")
            filename_rr="./自评文件集/"+bb+".txt"
            try:
                with open(filename_rr,"r",encoding='utf-8') as asdf:
                    j=asdf.read()
                    print(j)
                    input()
            except:
                print("您查询的文件不存在！请重新检查！")
                input()
    elif(cc=='b' or cc=='B'):
        dd=input("请问你要查询的日期是哪一天？请务必以“xxxx年，xx月，xx日。”的格式输入：")
        filename_tt="./自评文件集/"+dd+".txt"
        try:
            with open(filename_tt,"r",encoding='utf-8') as kkk:
                kj=kkk.read()
                print(kj)
                input()
        except:
            print("您想要查询的文件不存在！请重新检查！")
            input()
    else:
        print("你输入的不是a或者b!")
        input()
zi_ping()
