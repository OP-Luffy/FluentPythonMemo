
# -*- coding: utf-8 -*
#  用 函数对象 代替 设计模式中类的实例 #!/usr/bin/env python3
# ! memo 0001 mac下 如果 不 在第一行指定 #!/usr/bin/env python3, 则会出 Import Error; cannot import name abc
# !           但是windows下, 如果有了这一句, 则会在vscode的output窗口中显示乱码(即使拟显示的是英文)


# ! memo 0002 订单(order)的实例化
# !           首先, 实例化 Order 之前, 系统会议某种方式选择一种促销策略
# !           然后, 把选择的促销策略 传给 Order类的构造方法

from abc import ABC, abstractmethod
from collections import namedtuple

# ! memo 0003 命名元组(类名，属性名(域名))
# !           顾客类(名字，积分)
# !           Customer是一个类, 是 tuple的一个子类
Customer = namedtuple('Customer', 'name fidelity')


# ! memo 0004 商品(名称 product, 数量 quantity, 单价 price, 总价 total())
class Item: 

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    
    def total(self):
        return self.price * self.quantity

# ! memo 0005 订单(顾客customer, 购物车cart, 折扣策略promotion, 订单总价total(), 应缴费用due(), 实例对象显示__repr()__)    
# !           
# ! memo 0006 promotion 是 Promotion抽象基类, 
# !           这类仅仅只需实现一个 discount()方法, 无需任何属性和其它方法
# !           为了计算折扣, 必须知道订单的信息:
# !                        计算 积分折扣 需要: 订单总价 order.total(), 
# !                        计算 单个商品数量>=20优惠折扣 需要: 订单中每个商品的数量 item.quantity
# !                        计算 大订单(不同商品的数量大于100个)折扣 需要: 不用商品的数量
# !           Promotion的构造 需要知道 订单, 即, Promotion(self, order)
# !           从而其discount()方法可以调用订单信息, 即, discount(order)

class Order: 

# ! memo 0007 购物车是item的容器 cart = [item1, item2, ...]
    def __init__(self, customer, cart, promotion = None):
        self.customer = customer
        self.cart = list(cart)       # ! memo 0008 如果 就买了一个商品,即,入参 cart = item
        self.promotion = promotion   # !           list(cart) = list(item) 
                                     # !           这里 list() 就是保证 cart 是一个列表, 
                                     # !           即使只有一个 item
    
    def total(self):
        if not hasattr(self, '__total'):                            # ! memo 0009 如果一个订单的总价 __total还没有计算,
            self.__total = sum(item.total() for item in self.cart)  # !           则订单的total这个方法会累加各个item.total()计算
        return self.__total                                         # !           如果订单具有总价 __total 塑性, 说明算过了, 直接返回即可
    
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self) #! memo 0010 此处订单中 promotion.discount(self)   
        return self.total() - discount               #!           呼应 Promotion(self, order), 
                                                     #!                discount(order)
    
    def __repr__(self):
        fmt = '<Order total: {:.2f} due : {:.2f}'
        return fmt.format(self.total(), self.due())

print('---------- list(list(list(A))) = list(A) -------------')
print( list(list( [1, 2, 3] )), list([1, 2, 3]))

class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        """ 返回折扣金额 """

class FidelityPromo(Promotion):
    """ 为积分 >= 1000的顾客 提供 5% 折扣 """
    def discount(self, order):
        return order.total() * 0.5 if order.customer.fidelity >= 1000 else 0

class BulkItemPromo(Promotion):
    """ 
    单个商品数量 >= 20 提供10%折扣 
    注意: 这种折扣可以累加. 如果商品A数量超过20了, 则打折10%, 如果商品B数量超过20了, 则打折10%, 这样总折扣应为 20% 
    """
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * 0.1
        return discount

class LargeOrderPromo(Promotion):
    """ 订单中不同商品的数量 >= 10 提供 7% 折扣 """
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * 0.07
        return 0

print('------------ 示例 6-1 实现 Order 类，支持插入式折扣策略 --------------')
print('------------ 示例 6-2 使用不同促销折扣的 Order 类示例   --------------')

joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [Item('banana', 4, .5), Item('apple', 10, 1.5), Item('watermelon', 5, 5.0)]

print(Order(joe, cart, FidelityPromo()))
print(Order(ann, cart, FidelityPromo()))

bulk_item_cart = [Item('banana', 30, .5), Item('apple', 10, 1.5)]
print(Order(joe, bulk_item_cart, BulkItemPromo()))

long_order_cart = [Item(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order_cart, LargeOrderPromo()))

