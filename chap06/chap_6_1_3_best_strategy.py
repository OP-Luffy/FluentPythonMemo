# -*- coding: utf-8 -*

from chap_6_1_2_strategy_using_funcs import (Order, joe, long_order_cart,  #! memo 1 导入方式(1): from 模块名 import 函数名; 调用时可直接用 函数名   
                                             fidelity_promo,      
                                             bulk_item_promo,     
                                             large_order_promo)
print(fidelity_promo)   


# import chap_6_1_2_strategy_using_funcs as chap612 #! memo 2 导入方式(2): import 模块名; 调用时得用 模块名.函数名   
#                                                   #! 如果采用这种导入方式, 
#                                                   #! 就得用 chap612.fidelity_promo
#                                                   #!        chap612.bulk_item_promo 
# print(chap612.fidelity_promo)                     #!        chap612.large_order_promo



promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    """
    选择可用的最大的折扣函数
    """
    return max(promo(order) for promo in promos)

print(Order(joe, long_order_cart, best_promo))
