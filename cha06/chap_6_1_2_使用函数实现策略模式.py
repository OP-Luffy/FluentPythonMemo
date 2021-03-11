
# ! memo 0001 只有方法的类 ---> 函数
'''
在经典的策略模式中, 每个具体策略都是一个类, 但都只定义了一个方法, 即 discount. 策略实例没有状态（没有实例属性）. 
你可能会说，它们看起来像是普通的函数.
的确如此, 我们可以, 把具体策略换成了简单的函数，而且去掉了 Promo 抽象类。
'''

print('------------ 示例 6-3 使用函数实现折扣策略 + Order类 --------------')

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

print(Order(joe, cart, fidelity_promo)) #! memo 0005 对比经典策略模式 Order(joe, cart, FidelityPromo())
print(Order(ann, cart, fidelity_promo)) #!                           Order(ann, cart, FidelityPromo()) 
                                        #!                           FidelityPromo()对象被创建了两次,造成消耗
                                        #!                           各个策略函数在 Python 编译模块时只会创建一次
                                        #!                           普通的函数(相对于类的函数)是 可共享的对象,可以同时在多个上下文(oder)中使用

bulk_item_cart = [Item('banana', 30, .5), Item('apple', 10, 1.5)]
print(Order(joe, bulk_item_cart, bulk_item_promo))

long_order_cart = [Item(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order_cart, large_order_promo))

