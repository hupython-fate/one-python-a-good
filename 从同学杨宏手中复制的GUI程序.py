import threading
import time
import random
import tkinter as tk
from tkinter import ttk
#导入必要的库。

# 屏幕尺寸
SCREEN_W, SCREEN_H = 0, 0#定义两个变量。
try:
    root = tk.Tk()#创建一个窗口对象。
    root.withdraw()
    SCREEN_W = root.winfo_screenwidth()
    SCREEN_H = root.winfo_screenheight()
    root.destroy()
except:
    SCREEN_W, SCREEN_H = 1920, 1080  # 若获取失败，使用默认值


# 窗口大小
WINDOW_W, WINDOW_H = 120, 60
desired_points = 100 # 心形点数，可调整


def generate_heart_points(num_points, screen_w, screen_h, window_w, window_h):
    points = []
    center_x = screen_w // 2
    center_y = screen_h // 2
    for i in range(num_points):
        t = i / num_points * 2 * 3.14159
        x = 16 * (pow(math.sin(t), 3))
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        # 缩放和平移
        scale = min(screen_w // 40, screen_h // 40)
        x = center_x + x * scale
        y = center_y + y * scale
        # 确保窗口在屏幕内
        x = max(window_w // 2, min(x, screen_w - window_w // 2))
        y = max(window_h // 2, min(y, screen_h - window_h // 2))
        points.append((int(x), int(y)))
    return points
# 显示提示窗口的函数


def show_warn_tip(x, y, w, h):
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry(f"{w}x{h}+{x - w//2}+{y - h//2}")
    root.attributes('-topmost', True)
    # 随机颜色
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    root.configure(bg=f'#{r:02x}{g:02x}{b:02x}')
    # 随机提示语
    tips = [
        "保持好心情", "我想你了", "保持微笑", "天天都要元气满满", "别熬夜",
        "记得吃水果", "好好吃饭", "多喝水", "每天都要开心", "保持你的纯真",
        "你的微笑很特别", "要一直幸福哦", "想你的每一天", "照顾好自己", "记得想我"
    ]
    tip = random.choice(tips)
    label = ttk.Label(root, text=tip, font=('微软雅黑', 10), background=f'#{r:02x}{g:02x}{b:02x}')
    label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    # 使窗口可关闭
    def close():
        root.destroy()
    root.after(5000, close)  # 5秒后自动关闭，可调整
    root.mainloop()



if __name__ == "__main__":
    import math#导入数学库
    points = generate_heart_points(desired_points, SCREEN_W, SCREEN_H, WINDOW_W, WINDOW_H)
    #调用创建的第一个函数
    threads = []
    for (x, y) in points:
        t = threading.Thread(target=show_warn_tip, args=(x, y, WINDOW_W, WINDOW_H))
        threads.append(t)
        t.start()
        time.sleep(0.12)  # 放慢节奏，确保能看清文字
    # 所有弹窗都已创建，等待一段时间供阅读后统一关闭
    hold_seconds = 12  # 可调：全部出现后再停留的秒数
    time.sleep(hold_seconds)
    # 这里若要主动关闭所有窗口，因tkinter窗口是独立线程，可通过修改show_warn_tip的关闭逻辑实现批量关闭，
    # 此处简化为等待窗口自动关闭