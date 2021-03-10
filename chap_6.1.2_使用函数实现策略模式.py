

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

