import itertools

counter = itertools.count()

print(next(counter))
print(next(counter))
print(next(counter))

counter2 = itertools.count(start = 2, step = -0.5)

print(next(counter2))
print(next(counter2))
print(next(counter2))

data = [100, 200, 300, 400]
daily_data = list(zip(counter, data))
print(daily_data)

# 即使 python 内部是按顺序 一个一个地取, 第一个,第二个,第三个 元素...
# 其实调用的也是 next函数哦