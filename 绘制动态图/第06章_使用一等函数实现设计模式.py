
#  用 函数对象 代替 设计模式中类的实例

# ! memo 0002 订单(order)的实例化
# !           首先, 实例化 Order 之前, 系统会议某种方式选择一种促销策略
# !           然后, 把选择的促销策略 传给 Order类的构造方法

from abc import ABC, abstractmethod
from collections import namedtuple


Customer = namedtuple('Customer', 'name fidelity')
# ! 顾客: 

class Item: #! 0003 商品(名称, 数量, 单价, 总价())

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    
    def total(self):
        return self.price * self.quantity
    
class Order: # 订单(顾客, 购物车, 折扣策略)

    def __init__(self, customer, cart, promotion = None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
    
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self) #
        return self.total() - discount
    
    def __repr__(self):
        fmt = '<Order total: {:.2f} due : {:.2f}'
        return fmt.format(self.total(), self.due())

class 
