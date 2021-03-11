import chap_6_1_2_使用函数实现策略模式
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    """
    选择可用的最大的折扣函数
    """
    return max(promo(order) for promo in promos)


