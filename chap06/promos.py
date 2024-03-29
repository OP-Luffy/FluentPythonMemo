# -*- coding: utf-8 -*


from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class Item:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    
    def total(self):
        return self.price * self.quantity

class Order:
    def __init__(self, customer, cart, promotion = None): #! memo 0002 promotion是函数名
        self.customer = customer                          #!           这个函数的入参是一个订单对象
        self.cart = list(cart)
        self.promotion = promotion #! memo 0003 Order类有个属性, 这个属性就是一个函数(名)
    
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    
    def due(self): # 应缴费, __total是订单总价
        if self.promotion is None:
            discount = 0 # discount 折扣金额(元)
        else:
            discount = self.promotion(self) #! memo 0004 promtion 是函数名
        return self.total() - discount
    
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>' # fmt : format的简写
        return fmt.format(self.total(), self.due())

# ---------------- 用 函数 实现 折扣策略, 各个策略都是以订单对象为入参的函数 ------------------
def fidelity_promo(order): # 积分折扣函数
    """ 为积分 >= 1000的顾客 提供 5% 折扣 """
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order): # 单项商品量大批发折扣函数
    """ 
    单个商品数量 >= 20 提供10%折扣 
    注意: 这种折扣可以累加. 如果商品A数量超过20了, 则打折10%, 如果商品B数量超过20了, 则打折10%, 这样总折扣应为 20% 
    """
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1 
        return discount

def large_order_promo(order): # 大定单(总商品量大批发)折扣函数
    """ 订单中不同商品的数量 >= 10 提供 7% 折扣 """
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0


joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [Item('banana', 4, .5), Item('apple', 10, 1.5), Item('watermelon', 5, 5.0)]


bulk_item_cart = [Item('banana', 30, .5), Item('apple', 10, 1.5)]

long_order_cart = [Item(str(item_code), 1, 1.0) for item_code in range(10)]


print('------------ promos.py 被运行 --------------')
