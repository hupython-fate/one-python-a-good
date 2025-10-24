import asyncio
import aiohttp  #异步版 requests，基于 asyncio

async def ni_hao(name):
    print(f"你好，{name}")
    await asyncio.sleep(1)  # 模拟耗时操作
    print(f"Hello, {name}!")
    return f"问候 {name} 完成"


# 运行协程
async def main():
    result = await ni_hao("Alice")
    print(f"结果: {result}")

asyncio.run(main())