import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

plt.style.use('fivethirtyeight')

# ------------------------------------------------------


def func_called_each_frame(i):
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

plt.tight_layout()
plt.show()