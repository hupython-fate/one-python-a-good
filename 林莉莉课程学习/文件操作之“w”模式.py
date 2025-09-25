with open('../txt文件/第六次尝试.txt', "w", encoding='utf-8') as p:
    p.write('holle!\n')
    p.write('yoooo')
    #这段代码创建了一个.txt文件，并写入了两个字符串。

#"w"是写入模式（只写）
#‘a’是附加模式（不会清空原本文件的内容，而是会在原本的文件内容后面附加。

with open('../txt文件/第六次尝试.txt', 'a', encoding='utf-8') as l:
    l.write('这是附加的内容。')


#‘w’模式和‘a'模式一样，如果文件名不存在，那么就会帮你创建一个。
#还有，无论是“w"还是“a'模式，都无法使用read（），用了就会报错。

#"r+”支持同时读取文件。
with open('../txt文件/第六次尝试.txt', 'r+', encoding='utf-8') as k:

    print(k.read())
    k.write('你好！')