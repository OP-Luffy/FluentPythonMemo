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
    f1()
    f2()
    f3()
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


        


