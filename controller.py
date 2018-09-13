# -*- coding: utf-8 -*-

from salesEvent import SalesEvent
from transaction import Transaction
from random import randint
from random import random
from math import exp

class Controller():
    def __init__(self, view):
        
        self.view = view
        self.model = view.model
        
    def post_gui(self):
        self.view.after(3000, self.update_customer)
        self.view.after(20000, self.update_payday)
        self.view.after(100, self.proces_transactions)
        self.update_economy()
        
    def update_economy(self):
        self.view.lblMoney.config(text='Aktuel bundlinje: {:8d}'.format(int(self.model.get_total_accounting_value())))
        self.view.lblTotalBookCount.config(text='Antal bøger på lager: {}'.format(self.model.stock.get_total_item_count()))
        
        #Call again in 10 s
        self.view.after(10000, self.update_economy)
        
    def proces_transactions(self):
        #Search for an unfinished transaction
        for t in self.model.accounting:
            if t.state == Transaction.ST_READY:
                t.state = Transaction.ST_COMPLETE
        #Call again in 100 ms
        self.view.after(100, self.proces_transactions)
        
    def update_payday(self):
        total = 0
        for em in self.model.employees:
            t = self.model.get_transaction(Transaction.EMPLOYEE_SALARY, em.salary)
            t.state = Transaction.ST_READY
            total += em.salary
            em.paychecks.append(t)
        
        self.view.log_message('Lønudbetaling: {} kr\n'.format(total))
        self.update_economy()
        #Call again in 20 seconds
        self.view.after(20000, self.update_payday)
         
    def update_customer(self):
        #Everytime this function is called, we can 
        #simulate a customer.
        #The lower the markup, the more customers visit the store
        s = 1/(1+exp(3*self.model.markup.get()-6))
        if random() < s:
            sale = SalesEvent(self.model.get_transaction(Transaction.CUSTOMER_PURCHASE))
            
            #Buy between 1 and n books
            #n=2*number of employees => More workers, more chance
            #for customers to find the book they want..
            for i in range(randint(1,2*len(self.model.employees))):            
                item = self.model.stock.get_random_item_for_sale()
                if item != None:
                    sale.add_item(item)
                
            sale.finalize(self.model.markup.get())
            if sale.transaction.amount > 0:
                self.view.log_message('{}: En kunde købte bøger for {:d} kr\n'.format(sale.transaction.transactionId, int(sale.transaction.amount)))
                self.auto_restock()
                
            self.update_economy()
        
        #Call again in 3 seconds
        self.view.after(3000, self.update_customer)
    
    def validate_new_employee(self, dlg, name, salary):
        if name == '':
            return self.view.error('Navn er ikke intastet')
        if any(char.isdigit() for char in name):
            return self.view.error('Ikke et validt navn')
            
        if salary == '':
            return self.view.error('Løn er ikke intastet')
        
        try:
            salary = int(salary)
        except ValueError:
            return self.view.error('Løn er ikke en talværdi')
        
        if salary < 0:
            return self.view.error('Løn må ikke være mindre end 0')
        
        self.model.add_employee(name, salary)
        dlg.destroy()
    
    def validate_update_employee(self, dlg, id, salary):
        
        # Kan godt regne med at den altid retunerer en ansat, men tjekker alligevel.
        if salary == '':
            return self.view.error('Løn er ikke intastet')
    
        try:
            salary = int(salary)
        except ValueError:
            return self.view.error('Løn er ikke en talværdi')
    
        if salary < 0:
            return self.view.error('Løn må ikke være mindre end 0')
        
        self.model.update_employee(id, salary)
        dlg.destroy()
    
    def auto_restock(self):
        if self.model.activate_auto_restock.get() == 1:
            total = self.model.stock.get_total_item_count()
            minimum = int(self.view.autoRestock.get())
            
            totalBought = 0
            totalSpent = 0
            
            while total < minimum:
                salesItem = self.model.stock.get_random_item()
                
                salesItem.stockCount += 1
                t = self.model.get_transaction(Transaction.STOCK_PURCHASE)
                
                t.amount = salesItem.price
                t.state = Transaction.ST_READY
                
                totalBought += 1
                totalSpent += t.amount
                
                total += 1
            
            if totalBought > 0:
                self.view.show_book_info(None)
                self.update_economy()
                
                if totalBought != 1:
                    self.view.log_message('Auto indkøb, ' + str(totalBought) + ' bøger købt, kostede ' + str(totalSpent) + ' kr\n')
                else:
                    self.view.log_message('Auto indkøb, ' + str(totalBought) + ' bog købt, kostede ' + str(totalSpent) + ' kr\n')
