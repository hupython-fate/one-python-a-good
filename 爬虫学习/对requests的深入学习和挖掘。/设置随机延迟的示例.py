import time
import random

for i in range(10):
    # 随机延迟1到3秒
    time.sleep(random.uniform(1, 3))
    # 发送请求