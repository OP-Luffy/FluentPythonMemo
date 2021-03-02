import itertools

# ! mem 0001 关于 count()

counter1 = itertools.count()

print(next(counter1))
print(next(counter1))
print(next(counter1))

counter2 = itertools.count(start = 2, step = -0.5)

print(next(counter2))
print(next(counter2))
print(next(counter2))

data = [100, 200, 300, 400]
daily_data = list(zip(counter1, data))
print(daily_data)

# 即使 python 内部是按顺序 一个一个地取, 第一个,第二个,第三个 元素...
# 其实调用的也是 next函数哦

# ! mem 0002 关于 zip() 和 zip_longest()
daily_data_default = list( zip(range(10), data)) # 默认按短的iterable来匹配
daily_data_longest = list( itertools.zip_longest(range(10), data)) # 按长的来iterable来配对

print(daily_data_default)
print(daily_data_longest)


# ! mem 0003 cycle()
counter_cycle = itertools.cycle([1,2,3])
counter_cycle = itertools.cycle(('on', 'off'))
print(next(counter_cycle))
print(next(counter_cycle))
print(next(counter_cycle))
print(next(counter_cycle))

# ! mem 0004 repeat()
counter_repeat = itertools.repeat('Hello')
counter_repeat = itertools.repeat(9, times = 3)
print(next(counter_repeat))
print(next(counter_repeat))
print(next(counter_repeat))
# print(next(counter_repeat))
# StopIteration

# ! mem 0005 map(fun,xi,yi) = fun(xi,yi)
counter = itertools.count()
square = map(pow, range(10), itertools.repeat(2))
print(list(square))

# ! mem 0006 starmap(fun,[(x1,y1),(x2,y2)]) = a iterable has values : fun(x1,y1), fun(x2,y2),

lis_starmap = itertools.starmap(pow, [(1,1), (2,2), (3,3)])
print(next(lis_starmap))

# ! mem 0007 combinations(), permutations(), combinations_with_replacement
# ! mem 0008 所有iterable都可以用next()
letters = ['a', 'b', 'c', 'd']
numbers = [0, 1, 2, 3]
names = ['Xinxin', 'Guo']

result_comb = itertools.combinations(letters, 2)
result_comb = itertools.permutations(letters, 2)
result_comb = itertools.product(letters, repeat = 3)
result_comb = itertools.combinations_with_replacement(letters, 2)

print(next(result_comb))

for item in result_comb:
    print(item)

# ! mem 0009 chain()
# !          当要合并的iterable很大时, + 的效率较低
# !          这时应当用 chain(), 无需担心要合并的iterable很大, 每次我就用一个
combined_inefficient = letters + numbers + names

combined = itertools.chain(letters, numbers, names)
print(next(combined))

# ! mem 0010 islice()
sliced = itertools.islice(range(10), 4, 5, 2)
print(next(sliced))









