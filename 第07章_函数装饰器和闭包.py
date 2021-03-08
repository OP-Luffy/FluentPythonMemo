# ====================================================================================
# 示例  7-1 　装饰器通常把函数替换成另一个函数
# ====================================================================================
def deco(func):
    def inner():
        print('running inner()')
    return inner

# ! ------------------------------------
# ! mem 0001. 通过 语法糖 来施加 装饰器
# ! ------------------------------------

@deco
def target_sugar():
    print('running target_sugar')

target_sugar()
# running inner() 
# 装饰器 deco 修饰了 targer,似乎应返回 'running target()'
# 但 在装饰器的定义中, 装饰器无论装饰谁, 返回的都是 inner

# ! ------------------------------------
# ! mem 0002. 通过 函数调用 来施加 装饰器
# ! ------------------------------------

def target_func_call():
    print('running target_func_call')

target_func_call = deco(target_func_call)
# Function decorators let us “mark” functions in the source code to enhance their behavior in some way.
# target_func_call(装饰后的) = deco(target_func_call(未装饰的))
# 装饰前后的函数是同名函数
# 装饰不会执行函数,调用装饰后的同名函数才会执行

target_func_call()
# running inner() 


# ====================================================================================
# 7.2   Python何时执行装饰器
# ====================================================================================
# ! mem 0003 a 装饰器 在加载模块时 立即执行
# !          b 装饰器的一个关键特性是，它们在被装饰的函数定义之后 立即运行。 这通常是在 导入时(即 加载模块时)
# !          c 注册装饰器(register)原封不动地返回被装饰的函数，但是这种技术并非没有用处.

registry = []
def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func # 注册装饰器(register)原封不动地返回被修饰函数(func)
                # 装饰器 并没有 把被装饰的函数 变成 另一个函数，装饰的是func，返回的还是func
	            # 被装饰后的函数仍然指向的是原函数的引用，而不是返回指向一个fake_func

def f1():
    print('running f1()')
f1 = register(f1)

@register
def f2():
    print('running f2()')

def f3():
    print('running f3()')

def main():
    print('running main()')
    print('registry ->', registry)
    f1() # 此语句执行，就仅仅是在执行f1，
    f2() #           不会执行 ： print('running register(%s)' % func)
    f3() #                     registry.append(func)
if __name__ == '__main__':
    main()

'''
running inner()
running inner()
running register(<function f1 at 0x7f9ae57bf790>)
running register(<function f2 at 0x7f9ae57bf820>)
running main()
registry -> [<function f1 at 0x7f9ae57bf790>, <function f2 at 0x7f9ae57bf820>]
running f1()
running f2()
running f3()
'''

# ====================================================================================
# 7.4 　变量作用域规则
# ====================================================================================
# ! 为了理解闭包，我们要退后一步，先了解 Python中的 变量作用域。

def f1(a):
    print(a)
    print(b)

#  f1(3)
# NameError: name 'b' is not defined

b = 6
f1(3)


def f2(a):
    print(a)
    print(b) 
    b = 9 

# ! 0004 : a 因为在函数的 定义体中 给b赋值了, 所以b是局部变量
# !        b 但应该先赋值在调用. 上面程序先调用后赋值,则就错了

# f2(3)
# UnboundLocalError: 
# local variable 'b' referenced before assignment

c = 6
def f3(a):
    print(a)
    global c
    print(c) 
    c = 9 
f3(3) # 输出 3, 6
f3(3) # 输出 3, 9
# ! mem 0005 : a 即使在函数的 定义体中 给c赋值了, 
# !              但早已声明c乃全局变量
# !              故c是全局变量, 在定义体中 给c 赋值, 修改了的是全局变量c




# ====================================================================================
# 7.5　  闭包
# ====================================================================================
# ! mem 0006 :  a 只有涉及嵌套函数时才有闭包问题
# !             b 闭包: 指延伸了作用域的函数
# !                     函数定义体中 引用了 不在定义体中定义的非全局变量


# ---------------- 示例 7-8 : 计算移动平均值(通过 类 实现)
class Averager():

    def __init__(self):
        self.series = []
    
    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)

avg_obj = Averager()
print(avg_obj(10), avg_obj(11), avg_obj(12))

# ---------------- 示例 7-9 : 计算移动平均值(通过 高阶函数 实现)
def make_averager():
    # ------------------------- 闭包
    series = []
    
    def averager(new_value):         # ! 0007  局部变量 ≠ 自由变量
        series.append(new_value)     # !       a. series 是 自由变量(free variable): 指未在本地作用域中绑定的变量 (avg.__code__.co_freevars)
        total = sum(series)          # !       b. new_value 和 total 都是局部变量 (avg.__code__.co_varnames)
        return total/len(series)     # !       c. 如果这里的series一旦赋值,则它就变成了局部变量
    return averager
    # ------------------------- 闭包 # !       e. 可以通过nonlocal关键字把一个变量标记为自由变量

avg_fun = make_averager()
print(avg_fun(10), avg_fun(11), avg_fun(12))

# 这两个示例有共通之处： (1) 调用Averager() 或make_averager() 得到一个可调用对象avg
#                       (2) 它会更新历史值，
#                       (3) 计算当前均值

# ---------------- 示例 7-13 : 计算移动平均值的高阶函数,不保存所有历史值,但有Bug
def make_averager_bad():
    count = 0
    total = 0

    def averager(new_value):
        count += 1              #! mem 0008:  对count和total赋值了, 则它们都变成了局部变量
        total += new_value      #!       示例7-9 没遇到这个问题，因为我们没有给series赋值,我们只是调用series.append
        return total/count
    return averager

# avg_bad = make_averager_bad()
# print(avg_bad(10), avg_bad(11), avg_bad(12))
# UnboundLocalError: local variable 'count' referenced before assignment


# ---------------- 示例 7-14 : 计算移动平均值, 不保存所有历史, 使用 nonlocal 修正 7-13的Bug

def make_averager_good():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total/count
    return averager           #! mem 0010: 这里返回的 是averager, 不是 averager(), 没有执行哦

avg_good = make_averager_good()
print(avg_good(10), avg_good(11), avg_good(12))

# ====================================================================================
# 7.7　  实现一个简单的装饰器
# ====================================================================================
# ! mem 0011 老式的 % 字符串格式化: a. 以小数点为界, 
# !                                b. 前面: 对齐方式(-,0,+,空格) + 数据宽度; 
# !                                c. 后面: 精度(小数点后保留几位小数)
print('%09.3f'  % 1.234 ) #    0:补, 9:宽度, .:界限, 3:精度 
print('%09.3f'  % -12.34) # 空格:正数加个空格,从而与负数对齐
print('% 9.3f'  % -12.34) # 空格:正数加个空格,从而与负数对齐

import time

def clock_naive(func):               #! memo 0012 分清装饰器的参数和原函数的参数: a. 装饰器本身是个函数, 其参数为被装饰函数的函数名称
    def fake_func(*args):      #!                                          b. 原函数的参数 不受影响
        t0 = time.perf_counter() # perf: performance 返回性能计数器的值（以小数秒为单位）作为浮点数，即具有最高可用分辨率的时钟
        result = func(*args)                                                #! 原函数功能
        elapsed = time.perf_counter() - t0                                  #! 增强
        name = func.__name__                                                #! 增强
        arg_str = ', '.join(repr(arg) for arg in args)                      #! 增强
        print( '[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))  #! 增强 : [] 中括号; s:表示second 函数名(输入) -> 输出
        return result                                                       #! 原函数功能
    return fake_func


def snooze(seconds):
    time.sleep(seconds)
snooze = clock_naive(snooze)

@clock_naive
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)

print('*' * 40, 'Calling snooze(0.123)')
snooze(0.123)
print('*' * 40, 'Calling factorial(6)' )
print('6! = ', factorial(6))

print(factorial.__name__)
# 输出 fake_func

#! memo 0013 a. 函数factorial被修饰后,虽然名称没变,但其实它实际上是对修饰后函数(fake_factorial)的引用
#!           b. 装饰器的典型行为:
#!              b1. 把 被装饰函数 替换成 新函数
#!              b2. 二者接受相同的参数
#!              b3. 通常返回被装饰函数 本该 返回的值
#!              b4. 增加一些额外操作


#! memo 0014 clock_naive 装饰器有几个缺点：
#!                                      1. 不支持关键字参数
#!                                      2. 遮盖了原函数的__name__ 和__doc__ 属性
#! memo 0015 使用functool.wraps装饰器:
#!                                      1. 把原函数(func)的相关属性复制到 fake_func 中
#!                                      2. 正确处理 关键字参数
import time
import functools

def my_wrap(func):
    @functools.wraps(func)              #! memo 0016 在哪里使用 functool.wraps 装饰器 ?
    def fake_func(*args, **kwargs):     #!           再次强调: 装饰器 是一个 函数
        t0 = time.time()                #!           在自定义装饰器函数(my_wrap)的第一行
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        funcname = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s = %r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, funcname, arg_str, result))
        return result
    return fake_func

# ====================================================================================
# 7.8　 标准库中的装饰器
# ====================================================================================
        
# ! memo 0017   使用functools.lru_cache() (函数缓冲装饰器) 做备忘
# !             1 函数工具箱中的 装饰器, 来优化函数
# !             2 装饰器 都是 函数装饰器, 都是用来装饰函数, 以增强函数功能的
# !             3 它把 耗时的函数的结果 保存起来，避免 相同的参数时 重复计算
# !             4 lru = “Least Recently Used"

# ---------------- 示例 7-18:　生成第n个斐波纳契数，递归方式非常耗时(相同的入参,反复计算)
def clock(func):
    @functools.wraps(func)              
    def fake_func(*args, **kwargs):    
        t0 = time.time()               
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        funcname = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s = %r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, funcname, arg_str, result))
        return result
    return fake_func
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

print('---------------- out 7-18 ----------------')
print(fibonacci(6))

# ---------------- 示例 7-19　使用缓存实现，速度更快
import functools

@functools.lru_cache()
@clock 
                 # 这里叠放了两个装饰器
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
print('---------------- out 7-19 ----------------')
print(fibonacci(6))

# ! memo 0019   functools.lru_cache(maxsize=128, typed=False) 的入参:
# !             a. maxsize
# !                1 maxsize 参数指定存储多少个调用的结果
# !                2 缓存满了之后,旧的结果会被扔掉,腾出空间
# !                3 为了得到最佳性能，maxsize 应该设为2 的幂。
# !             b. typed
# !                1 是否把不同参数类型得到的结果分开保存
# !                2 即把通常认为相等的浮点数和整数参数（如1 和1.0）区分开
# !             c. 哪些函数可以利用这个缓冲装饰器来提高性能?
# !                1 因为 lru_cache 使用字典存储结果, 字典key由函数入参(位置或关键字入参)生成
# !                2 所以 只有函数的入参是 可散列 的时, 才能使用缓冲装饰器来装饰以提高性能

# ! memo 0020 可散列
'''
1. 不严谨但易懂的解释：

   一个对象在其生命周期内，如果保持不变，就是hashable（可哈希的）。

   hashable ≈ imutable , 可哈希 ≈ 不可变

   在Python中：

   list、set和dictionary 都是可改变的，
   比如可以通过list.append()，set.remove()，dict['key'] = value对其进行修改，
   所以它们都是不可哈希的；

   而tuple和string是不可变的，只可以做复制或者切片等操作，所以它们就是可哈希的。


2. 较严格的解释:

   如果一个对象在其生命周期内，其哈希值从未改变(这需要一个__hash__()方法)，
   并且可以与其他对象进行比较(这需要一个__eq__()或__cmp__()方法)，
   那么这个对象就是可哈希的。
   哈希对象的相等意味着其哈希值的相等。

   可哈希性的对象可以用作dictionary键和set元素，因为这些数据结构在内部使用了哈希值。

参见:详解Python中的可哈希对象与不可哈希对象(一)(二).pdf
'''

print(hash((1, 2, (3,4))))
# print(hash((1, 2, [3,4]))) #输出: TypeError: unhashable type: 'list'

# ====================================================================================
# 7.8.2　单分派 泛函数
# ====================================================================================

'''
--------------------------------------------------------------
def process(data):
    if cond0 and cond1:
        # apply func01 on data that satisfies the cond0 & cond1
        return func01(data)
    elif  cond2 and cond3:
        # apply func23 on data that satisfies the cond2 & cond3
        return func23(data)
    elif  cond4 and cond5:
        # apply func45 on data that satisfies the cond4 & cond5
        return func45(data)
----------------------------------------------------------------
   This pattern gets tedious when the number of conditions and actionable functions
start to grow. I was looking for a functional approach to avoid deﬁning and calling
three diﬀerent functions that do very similar things. Situations like this is where
parametric polymorphism comes into play. The idea is, you have to deﬁne a single
function that will be dynamically overloaded with alternative implementations based
on the type of the function arguments.

    Function overloading is a speciﬁc type of polymorphism where multiple functions
can have the same name with diﬀerent implementations. Calling an overloaded
function will run a speciﬁc implementation of that function based on some prior
conditions or appropriate context of the call. When function overloading happens
based on its argument types, the resulting function is known as generic function.
Let’s see how Python’s  singledispatch  decorator can help to design generic
functions and refactor the icky code above. 
'''

# ---------------- Example-1: 用 if/elif+多个类似的函数名 实现 内置类型 的多态处理

def process_with_if(num):
    if isinstance(num, int):
        return process_int(num)
    elif isinstance(num, float):
        return process_float(num)

def process_int(num):
    return(f"Integer number {num} has been processed successfully!")

def process_float(num):
    return(f"Float number {num} has been processed successfully!")

print('---------------- out 多态 例-1: if/elif 实现 ----------------')
print(process_with_if(12))
print(process_with_if(12.1))
# 输出
# Integer number 12 has been processed successfully!
# Float number 12.1 has been processed successfully!

# ---------------- Example-2: 用 Singledispatch 来多态地处理 内置类型
from functools import singledispatch

@singledispatch
def process_num(num=None):
    raise NotImplementedError("Implement function process ")

@process_num.register(int)
def _(num):
    return(f"Integer number {num} has been processed successfully!")

@process_num.register(float)
def _(num):
    return(f"Float number {num} has been processed successfully!")


print('---------------- out 多态 例-2: @Singledispatch 实现 ----------------')
print(process_num(12))
print(process_num(12.1))
# print(process_num('12'))
# NotImplementedError: Implement function process 

# 输出
# Integer number 12 has been processed successfully!
# Float number 12.1 has been processed successfully!

# ---------------- Example-3: Singledispatch with custom argument type
def process_pet_with_if(data: dict):
    if data["genus"] == "Felis" and data["bucket"] == "cat":
        return process_cat(data)
    elif data["genus"] == "Canis" and data["bucket"] == "dog":
        return process_dog(data)
def process_cat(data: dict):
    # processing cat
    return "Cat data has been processed successfully!"
def process_dog(data: dict):
    # processing dog
    return "Dog data has been processed successfully!"

if __name__ == "__main__":
    cat_data = {"genus": "Felis", "species": "catus", "bucket": "cat"}
    dog_data = {"genus": "Canis", "species": "familiaris", "bucket": "dog"}
    # using process
    print('---------------- Example-3: Singledispatch + custom type')
    print(process_pet_with_if(cat_data))
    print(process_pet_with_if(dog_data))

#  输出 
# >>> Cat data has been processed successfully!
# >>> Dog data has been processed successfully!

# ---------------- Example-4: Singledispatch + custom type + dataclass
from functools import singledispatch
from dataclasses import dataclass
@dataclass
class Cat:
    genus: str
    species: str
@dataclass
class Dog:
    genus: str
    species: str
@singledispatch
def process(obj=None):
    raise NotImplementedError("Implement process for bucket")
@process.register(Cat)
def sub_process(obj):
    # processing cat
    return "Cat data has been processed successfully!"
@process.register(Dog)
def sub_process(obj):
    # processing dog
    return "Dog data has been processed successfully!"
if __name__ == "__main__":
    cat_obj = Cat(genus="Felis", species="catus")
    dog_obj = Dog(genus="Canis", species="familiaris")
    print('---------------- Example-4: Singledispatch + custom type + dataclass')
    print(process(cat_obj))
    print(process(dog_obj))




# ====================================================================================
# 7.10　  参数化装饰器
# 7.10.1　一个参数化的注册装饰器
# ====================================================================================

# ---------------- 示例 7-18:　生成第n个斐波纳契数，递归方式非常耗时(相同的入参,反复计算)

registry = set()

def register(active=True):
	def decorate(func):
		print('running register(active=%s)-->decorate(%s)' %(active,func))
		if active:
			registry.add(func) 
		else:
			registry.discard(func)
		return func    	# 立马返回原函数
	return decorate 	# 返回装饰器. 装饰器会做什么？先根据入参决定是否注册，再返回原函数


@register(active=False) 
def f1():
	print('running f1()')

@register()
def f2():
	print('running f2()')

def f3():
	print('running f3()')

print('---------------- out 7-23 ----------------')
print('running main()') 
print('registry ->',registry) 
f1() # 此语句执行, 仅仅是在执行f1.
f2() #            不会执行: print('running register(%s)' % func)
f3() #                      registry.append(func)

# ====================================================================================
# 7.10.2　参数化clock装饰器
# ====================================================================================

# -------------- 示例 7-25　clockdeco_param.py 模块：参数化 clock 装饰器
print('---------------- 7-25 deco_par with default par ----------------')
import time

DEFAULT_FMT = '[{elapsed:0.8f} seconds] {name}({args}) -> {result}'

def AddPar2Decoate(par = DEFAULT_FMT):
    def decorate(func): # decorate(func, par)
        # print(par)
        def fakeFunc(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(par.format(**locals())) # fmt.format( name = func实参, args = _args实参, ...)
            return _result
        return fakeFunc
    return decorate
# ! memo 0021 : 掌握两层和三层的一般就足够了
# ! 一般装饰器是两层嵌套函数,带参数的装饰器又多了一层来传递par


@AddPar2Decoate() # ! memo 0022 我第一次丢了括号,写成了 @AddPar2Decoate, 结果没有输出任何东东
def snooze(seconds):
    time.sleep(seconds)
for i in range(3):
    snooze(.123)



print('---------------- 7-26 deco_par with user par ----------------')
@AddPar2Decoate('{name} : {elapsed}  s') # ! memo 0022 我第一次丢了括号,写成了 @AddPar2Decoate, 结果没有输出任何东东
def snooze(seconds):
    time.sleep(seconds)
for i in range(3):
    snooze(.123)

print('---------------- 7-27 deco_par with user par ----------------')
@AddPar2Decoate('{name}({args})  dt = {elapsed:0.3f}s') # ! memo 0022 我第一次丢了括号,写成了 @AddPar2Decoate, 结果没有输出任何东东
def snooze(seconds):
    time.sleep(seconds)
for i in range(3):
    snooze(.123)