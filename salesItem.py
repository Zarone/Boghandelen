# -*- coding: utf-8 -*-
class SalesItem:
    
    
    def __init__(self, itemId, name, group, price):
        self.itemId = itemId
        self.name = name
        self.itemGroup = group
        #The price is the price to purchase the books.
        #Books are later sold at a markup
        self.price = price
        self.stockCount = 0
        self.sales = 0
        
    def set_amount(self, n):
        self.stockCount = n
    
    @classmethod
    def copy(cls, c):
        s = SalesItem(c.itemId, c.name, c.itemGroup, c.price)
        return s