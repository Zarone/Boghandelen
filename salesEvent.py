# -*- coding: utf-8 -*-
from transaction import Transaction

class SalesEvent:
    
    def __init__(self, transaction):
        self.items = []        
        self.transaction = transaction
        
    def get_total_value(self, markup):
        sum = 0
        for i in self.items:
            sum += i.price * i.stockCount * markup
        return sum
    
    def add_item(self, salesItem):
        self.items.append(salesItem)
        salesItem.sales += 1
        
    def finalize(self, markup):
        self.transaction.amount = self.get_total_value(markup)
        self.transaction.state = Transaction.ST_READY
        