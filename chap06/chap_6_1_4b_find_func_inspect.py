# -*- coding: utf-8 -*
import inspect, promos


print('----- 示例 6-8　内省单独的 promotions 模块，构建 promos 列表 ----')
plis = [func for name, func in 
                inspect.getmembers(promos, inspect.isfunction)
                if name != 'namedtuple'] 

print(plis)
# print(pm.Order, pm.joe, pm.long_order_cart)

def best_promo_inspect(order): 
    """选择可用的最佳折扣 
    """ 
    return max(i(order) for i in plis)
best = promos.Order(promos.joe, promos.long_order_cart, best_promo_inspect)
print(str(best))



#! memo 0002 关于导入
#! (1) ---------- wokrs ----------------
# import math
# print(inspect.getmembers(math, inspect.isroutine))

#! (2) ---------- fails ----------------
# from math import *
# print(inspect.getmembers(math, inspect.isroutine))

#! (3) ---------- works ----------------
# from math import *
# import math
# print(inspect.getmembers(math, inspect.isroutine))