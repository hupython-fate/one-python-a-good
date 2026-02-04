f=open('../../txt文件/一次尝试.txt', 'r', encoding='utf-8')
x=f.read()#第一次read时就已经读到结尾了。
print(x)
y=f.read()#再次读取会返回空字符串。
print(y)
#第三个参数encoding虽然是可选的，但是有时编码方式会变成其它，所以还是加上为好。
#如果不填如第三个参数，那么很可能会报错。
f.close()#关闭文件，释放资源。


'''
在文件体积特别大的情况下，最好不用read方法，比如文件有15GB时，因为会占用很大的内存。
如果想要读取文件得一部分，而不是全部的文件，那么可以在read()的括号里加入数字，表示读取多少字节。
'''

m=open('../../txt文件/第二次尝试.txt', 'r', encoding='utf-8')
print(m.read(10))#读取1~10字节的文字。
#为什么是空的呢？因为第一次读已经读到结尾了。所以要换下一个文件。
print(m.read(20))#读取11~31字节的文字。


#尝试一下readline方法。
print(m.readline())#会读取一行文字内容，并打印.#输出的是“开国何茫然。”

#whlie循环与print（m.readline())的结合。
ppp=m.readline()
while ppp!='':#''中间没有空格，就是连续的两个单引号。
    print(ppp)
    ppp=m.readline()
m.close()#关闭文件，释方资源。



#尝试一下readlines的方法，它会读取全部的文件内容，并把每行当作列表（list)元素返回。

k=open('../../txt文件/第三次尝试.txt', 'r', encoding='utf-8')
jjj=k.readlines()
print(jjj)
k.close()#关闭文件，释方资源。




#readlines方法与for循环结合。
d=open('../../txt文件/第四次尝试.txt', 'r', encoding='utf-8')
ddd=d.readlines()#这一行输出的是列表。
for dddss in ddd:
    print(dddss)
d.close()#关闭文件，释方资源。

'''
每次在open文件后，完成读写操作后，都要在后面加上close（），有些麻烦。
所以还有一种更简便的方法，with关键字。
例子如下：
'''


with open('../../txt文件/第五次尝试.txt', 'r', encoding='utf-8') as gu:
    print(gu.read())#对文件的操作。
    #带缩进的内容会在执行完后自动关闭文件，释放资源。


