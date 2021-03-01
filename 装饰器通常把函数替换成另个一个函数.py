# =====================================
# 示例  7-1 　装饰器通常把函数替换成另一个函数
# =====================================
def deco(func):
    def inner():
        print('running inner()')
    return inner

# ! ------------------------------------
# ! 1. 通过 语法糖 来施加 装饰器
# ! ------------------------------------

@deco
def target_sugar():
    print('running target_sugar')

target_sugar()
# running inner() 
# 装饰器 deco 修饰了 targer,似乎应返回 'running target()'
# 但 在装饰器的定义中, 装饰器无论装饰谁, 返回的都是 inner

# ! ------------------------------------
# ! 2. 通过 函数调用 来施加 装饰器
# ! ------------------------------------

def target_func_call():
    print('running target_func_call')

target_func_call = deco(target_func_call)

target_func_call()
# running inner() 
