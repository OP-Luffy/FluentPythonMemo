# ====================================================================================
# 示例  7-1 　装饰器通常把函数替换成另一个函数
# ====================================================================================
def deco(func):
    def inner():
        print('running inner()')
    return inner

# ! ------------------------------------
# ! 0001. 通过 语法糖 来施加 装饰器
# ! ------------------------------------

@deco
def target_sugar():
    print('running target_sugar')

target_sugar()
# running inner() 
# 装饰器 deco 修饰了 targer,似乎应返回 'running target()'
# 但 在装饰器的定义中, 装饰器无论装饰谁, 返回的都是 inner

# ! ------------------------------------
# ! 0002. 通过 函数调用 来施加 装饰器
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
# ! 0003 a 装饰器 在加载模块时 立即执行
# !      b 装饰器的一个关键特性是，它们在被装饰的函数定义之后 立即运行。 这通常是在 导入时(即 加载模块时)
# !      c 注册装饰器(register)原封不动地返回被装饰的函数，但是这种技术并非没有用处.

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
# ! 0005 : a 即使在函数的 定义体中 给c赋值了, 
# !          但早已声明c乃全局变量
# !          故c是全局变量, 在定义体中 给c 赋值, 修改了的是全局变量c





