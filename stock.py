# -*- coding: utf-8 -*-
from salesItem import SalesItem
from random import randint
import csv
import ast

class Stock:
    
    def __init__(self):
        self.inventory = []
        
    def get_itemGroup_list(self):
        itemGroupList = []
        for i in self.inventory:
            itemGroupList.append(i.itemGroup)
        return set(itemGroupList)
    
    def get_item_list(self, itemGroup):
        print(itemGroup)
        itemList = []
        for i in self.inventory:
            if i.itemGroup == itemGroup:
                itemList.append((i.name, i.itemId))
        return itemList
        
    def get_item_count(self, itemId):
        sum = 0
        for i in self.inventory:
            if i.itemId == itemId:
                sum += i.stockCount
        return sum
    
    def get_total_item_count(self):
        sum = 0
        for i in self.inventory:
            sum += i.stockCount
        return sum    
    
    def get_total_inventory_value(self):
        value = 0
        for i in self.inventory:
            value += i.stockCount * i.price
        return value

    def get_inventory_value(self, itemID):
        s = self.find_sales_item(itemID)
        res = 0
        if s is not None:
            res = s.stockCount * s.price
        return res
    
    def find_sales_item(self, itemID):
        res = None
        for i in self.inventory:
            if i.itemId == itemID:
                res = i
        return res
    
    def get_random_item(self):
        index = randint(0,len(self.inventory)-1)
        item = self.inventory[index]
        return item
    
    def get_random_item_for_sale(self):
        index = randint(0,len(self.inventory)-1)
        item = self.inventory[index]
        
        #We return a copy of the SalesItem, with a count
        #of 1, if a book can be sold, and 0 if not
        r = SalesItem.copy(item)
        if item.stockCount > 0:
            #The book is subtracted from the stock
            item.stockCount -= 1
            r.stockCount = 1
            return r
        else:
            r.stockCount = 0
            
        return None
        
    def build_initial_stock(self):
        
        with open('books.csv', newline='') as f:
            reader = csv.DictReader(f, delimiter=';')
            for book in reader:
                price = 0
                try:
                    price = int(book['list_price'])
                except:
                    pass
                
                descripion = None
                try:
                    description = ast.literal_eval(book['desc'].replace('=>', ':'))['Description']
                except:
                    pass
                
                author = None
                try:
                    author = description['Authored By']
                except:
                    pass
                    
                
                s = SalesItem(book['uniq_id'], book['name'], book['group'], price, author)
                self.inventory.append(s)
                if randint(0,10) < 1:
                    s.stockCount = randint(1,20)            
            
        
        
        
        
        
        
        
        
        
        
        
        
    