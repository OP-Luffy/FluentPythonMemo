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
# 7.2 Python何时执行装饰器
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






