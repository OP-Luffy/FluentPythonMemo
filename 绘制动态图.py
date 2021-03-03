import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

plt.style.use('fivethirtyeight')

# --------------------------------------------- 静态简单测试
xi_vals = [0, 1, 2, 3, 4, 5]
yi_vals = [0, 1, 3, 2, 3, 5]

plt.plot(xi_vals, yi_vals)
plt.tight_layout()

plt.pause(2)
plt.close('all')

# 在matplotlib中，轴Axes的位置以标准化图形坐标指定，
# 可能发生的情况是轴标签、标题、刻度标签等等会超出图形区域，导致显示不全。
# 命令tight_layout()自动调整子图参数，使之填充整个图像区域。


x_vals = []
y_vals = []

index = count()

def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0,5))
    plt.cla() # 每次画图 横纵坐标在变,所以清除掉
    plt.plot(x_vals, y_vals)

ani = FuncAnimation(plt.gcf(), animate, interval = 1000)


plt.plot(x_vals, y_vals)
plt.tight_layout()
plt.show()

# matplotlib.pyplot.cla() 方法清除當前座標軸，
# matplotlib.pyplot.clf() 方法清除當前圖形，
# matplotlib.pyplot.close() 方法關閉整個視窗。