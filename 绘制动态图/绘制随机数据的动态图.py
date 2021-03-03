import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

plt.style.use('fivethirtyeight')

# ---------------------------- 1. 静态简单测试 --------------------------
xi_vals = [0, 1, 2, 3, 4, 5]
yi_vals = [0, 1, 3, 2, 3, 5]

plt.plot(xi_vals, yi_vals)
plt.tight_layout()

# ! memo 0001.  plt.show(block=False)函数的参数block:
# !                 In non-interactive mode, 
# !                 display all figures and 
# !                 block(阻断) until the figures have been closed;
plt.show(block=False)
plt.pause(2)
plt.close()

# 在matplotlib中，轴Axes的位置以标准化图形坐标指定，
# 可能发生的情况是轴标签、标题、刻度标签等等会超出图形区域，导致显示不全。
# 命令tight_layout()自动调整子图参数，使之填充整个图像区域。

# ---------------------------- 2. 动态画图 --------------------------

xi = []
yi = []

index = count()

def func_called_each_frame(i):
    xi.append(next(index))
    yi.append(random.randint(0,5))
    plt.cla() # 每次画图 横纵坐标在变,所以清除掉
    plt.plot(xi, yi)

ani = FuncAnimation(plt.gcf(), func_called_each_frame, interval = 1000)


plt.plot(xi, yi)
plt.tight_layout()
plt.show()

# matplotlib.pyplot.cla() 方法清除當前座標軸，
# matplotlib.pyplot.clf() 方法清除當前圖形，
# matplotlib.pyplot.close() 方法關閉整個視窗。

# ---------------------------- 2. 监测文件,动态绘图 --------------------------



def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    plt.cla() # 每次画图 横纵坐标在变,所以清除掉

    plt.plot(x, y1, label = 'Channel 1')
    plt.plot(x, y2, label = 'Channel 2')

    plt.legend(loc = 'upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), func_called_each_frame, interval = 1000)


plt.plot(xi, yi)
plt.tight_layout()
plt.show()
