import asyncio

async def AAA():
    print("1")
    await asyncio.sleep(5)
    print("2")
    return

async def bbb():
    print("bbb开始。")
#把一个协程对象转化为一个task对象。
    task1=asyncio.create_task(AAA())##到这里时,代码不会进行跳转。
    #把AAA（）协程对象添加进事件循环。
    task2=asyncio.create_task(AAA())
    #一共创建了两个task对象。


    #task_list=[task1=asyncio.create_task(AAA()),task2=asyncio.create_task(AAA())]
    #上一行代码等价于上两行代码。


    print("BBB结束！")
    ret1=await task1#到这里时，代码会进行跳转，因为bbb(）协程进行了等待，事件循环会自动进行下一个可执行的协程，所以在bbb()协程等待时，会自动执行AAA()协程。
    #然后，第一个AAA（）协程进行了等待，所以自动执行第二个AAA()协程。
    ret2=await task2
    #done,pending=await asyncio.wait(task_list)
    print(ret1,ret2)#输出的是空值。


asyncio.run(bbb())#相当于这个时候，事件循环有三个协程。


#学到这里，我应该可以去实际应用异步编程了。7

'''感想是什么？AI终究不是人类，学习还是要找一些网课。'''