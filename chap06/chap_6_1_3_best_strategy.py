# from chap6 import *
import chap6

promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    """
    选择可用的最大的折扣函数
    """
    return max(promo(order) for promo in promos)

print(Order(joe, long_order_cart, best_promo))
