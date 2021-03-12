# -*- coding: utf-8 -*
import inspect
from chap_6_1_2_strategy_using_funcs import *


# promos = [fidelity_promo, bulk_item_promo, large_order_promo]

print(' ---- 示例 6-7　内省模块的全局命名空间，构建 promos 列表 ---')
# value = 字典[key]
promos = [ globals()[name] for name in globals()
           if name.endswith('_promo')
           and name != 'best_promo']
print(promos)
#! memo 0001 函数是一种对象:
#!           [<function fidelity_promo at 0x01EE41E0>, 
#!            <function bulk_item_promo at 0x01EE43D8>, 
#!            <function large_order_promo at 0x01EE4420>]
def best_promo(order):
    """
    选择可用的最大的折扣函数
    """
    return max(promo(order) for promo in promos)

print(Order(joe, long_order_cart, best_promo))
