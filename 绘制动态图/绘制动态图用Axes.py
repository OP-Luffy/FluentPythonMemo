import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import os

#! 注意两个目录: 工作目录 ≠ 当前文件目录
cwd = os.getcwd()   
curr_file_dir = os.path.dirname(__file__)

print({'cwd':cwd, 'curr file dir':curr_file_dir})


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def animate(i):
    pulled_dat = open(os.path.join(curr_file_dir,'sampleDat.txt'),'r').read()
    dat = pulled_dat.split('\n')
    xvec = []
    yvec = []
    for eachLine in dat:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xvec.append(int(x))
            yvec.append(int(y))
    ax1.clear()
    ax1.plot(xvec, yvec)

ani = animation.FuncAnimation(fig, animate, interval = 1000)

plt.show()