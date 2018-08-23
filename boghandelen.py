# -*- coding: utf-8 -*-
import tkinter as tk
from stock import Stock
from salesEvent import SalesEvent
from transaction import Transaction
from employee import Employee
from random import randint
from random import random
from math import exp

class Boghandelen(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()  
        
        self.accounting = []
        
        self.stock = Stock()
        self.stock.build_initial_stock()
        
        self.markup = tk.DoubleVar()
        self.markup.set(1.3)
            
        
        #Add two initial employees
        self.employees = []
        e1 = Employee("John", 500)
        self.employees.append(e1)
        e2 = Employee("Jane", 500)
        self.employees.append(e2)

        
        self.scale = float(1)/6
        self.build_GUI()
        
        #Start the timed events for the simulation
        self.after(3000, self.update_customer)
        self.after(20000, self.update_payday)
        self.after(100, self.proces_transactions)
        self.update_economy()
        
    def update_economy(self):
        self.lblMoney.config(text='Aktuel bundlinje: {:8d}'.format(int(self.get_total_accounting_value())))
        self.lblTotalBookCount.config(text='Antal bøger på lager: {}'.format(self.stock.get_total_item_count()))
        
        #Call again in 10 s
        self.after(10000, self.update_economy)
        
    def proces_transactions(self):
        #Search for an unfinished transaction
        for t in self.accounting:
            if t.state == Transaction.ST_READY:
                t.state = Transaction.ST_COMPLETE
        #Call again in 100 ms
        self.after(100, self.proces_transactions)
        
    def update_payday(self):
        total = 0
        for em in self.employees:
            t = self.get_transaction(Transaction.EMPLOYEE_SALARY, em.salary)
            t.state = Transaction.ST_READY
            total += em.salary
            em.paychecks.append(t)
        
        self.log_message('Lønudbetaling: {} kr\n'.format(total))
        self.update_economy()
        #Call again in 20 seconds
        self.after(20000, self.update_payday)
         
    def update_customer(self):
        #Everytime this function is called, we can 
        #simulate a customer.
        #The lower the markup, the more customers visit the store
        s = 1/(1+exp(3*self.markup.get()-6))
        if random() < s:
            sale = SalesEvent(self.get_transaction(Transaction.CUSTOMER_PURCHASE))
            
            #Buy between 1 and n books
            #n=2*number of employees => More workers, more chance
            #for customers to find the book they want..
            for i in range(randint(1,2*len(self.employees))):            
                item = self.stock.get_random_item_for_sale()
                if item != None:
                    sale.add_item(item)
                
            sale.finalize(self.markup.get())
            if sale.transaction.amount > 0:
                self.log_message('{}: En kunde købte bøger for {:d} kr\n'.format(sale.transaction.transactionId, int(sale.transaction.amount)))
                
            self.update_economy()
        
        #Call again in 3 seconds
        self.after(3000, self.update_customer)

     
    #This function acts as a transaction factory
    #All transactions should come from here,
    #to ensure correct processing
    def get_transaction(self, transactiontype, amount = 0):
        t = Transaction(transactiontype, amount)
        self.accounting.append(t)
        return t


    def get_total_accounting_value(self):
        value = 0
        for a in self.accounting:
            if a.state == Transaction.ST_COMPLETE:
                if a.transactionType == Transaction.CUSTOMER_PURCHASE:
                    #Customer purchases are added to the value
                    value += a.amount
                elif a.transactionType == Transaction.EMPLOYEE_SALARY:
                    #Salaries are subtracted
                    value -= a.amount
                elif a.transactionType == Transaction.CUSTOMER_RETURN:
                    #Returns are also subtracted
                    value -= a.amount
                elif a.transactionType == Transaction.STOCK_PURCHASE:
                    #Stock purchases are also subtracted
                    value -= a.amount
        return value
    
    def build_GUI(self):
        
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side = tk.BOTTOM)
        
        leftFrame = tk.Frame(bottomFrame)
        leftFrame.pack(side = tk.LEFT)
        
        rightFrame = tk.Frame(bottomFrame)
        rightFrame.pack(side = tk.RIGHT)
        
        topFrame = tk.Frame(self)
        topFrame.pack(side = tk.TOP)
        topSelectFrame = tk.Frame(topFrame)
        topSelectFrame.pack(side = tk.TOP)
        topLeftFrame = tk.Frame(topSelectFrame)
        topLeftFrame.pack(side=tk.LEFT)
        topRightFrame = tk.Frame(topSelectFrame)
        topRightFrame.pack(side=tk.RIGHT)
        topInfoFrame = tk.Frame(topFrame)
        topInfoFrame.pack(side=tk.BOTTOM)
        
        #Left buttonpanel
        btnShowEmployees = tk.Button(leftFrame, text='Vis ansatte', command=self.show_employees, width=int(70*self.scale))
        btnShowEmployees.pack(fill = tk.X)
        btnAddEmployees = tk.Button(leftFrame, text='Tilføj ansatte', command=self.add_employee, width=int(70*self.scale))
        btnAddEmployees.pack(fill = tk.X)
        self.lblMoney = tk.Label(leftFrame, text='Aktuel bundlinje: {}'.format(self.get_total_accounting_value()))
        self.lblMoney.pack(fill=tk.X)
        self.lblTotalBookCount = tk.Label(leftFrame, text='Antal bøger på lager: {}'.format(self.stock.get_total_item_count()))
        self.lblTotalBookCount.pack(fill=tk.X)
        
        self.slMarkup = tk.Scale(leftFrame, label=None, resolution=0.1, orient=tk.HORIZONTAL, from_=0, to=2, variable=self.markup)
        self.slMarkup.pack(fill = tk.X)
        
        self.console = tk.Text(rightFrame, width=int(430*self.scale))
        self.console.pack()
        
        lbl1 = tk.Label(topLeftFrame, text='Vælg kategori', width=int(70*self.scale), padx=10)
        lbl1.pack(side = tk.LEFT)
        
        self.categories = self.stock.get_itemGroup_list()
        
        scrollbar_c = tk.Scrollbar(topLeftFrame, orient=tk.VERTICAL)
        self.lbCategories = tk.Listbox(topLeftFrame, yscrollcommand=scrollbar_c.set, height=5, width=int(200*self.scale))
        scrollbar_c.config(command=self.lbCategories.yview)
        scrollbar_c.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbCategories.bind('<<ListboxSelect>>', self.update_book_list)
        self.lbCategories.pack(side=tk.LEFT, fill=tk.BOTH)
        for c in self.categories:
            self.lbCategories.insert(tk.END, c)
        
        lbl2 = tk.Label(topRightFrame, text='Vælg bog', width=int(70*self.scale), padx=10)
        lbl2.pack(side = tk.LEFT)
        
        scrollbar_t = tk.Scrollbar(topRightFrame, orient=tk.VERTICAL)
        self.lbBooks = tk.Listbox(topRightFrame, yscrollcommand=scrollbar_t.set, height=5, width=int(200*self.scale))
        scrollbar_t.config(command=self.lbBooks.yview)
        scrollbar_t.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbBooks.bind('<<ListboxSelect>>', self.show_book_info)
        self.lbBooks.pack(side=tk.LEFT, fill=tk.BOTH)
        
        self.lblBookSales = tk.Label(topInfoFrame, text='Antal solgte: ', width=int(300*self.scale), justify=tk.LEFT)
        self.lblBookSales.pack(side=tk.BOTTOM)
        self.lblBookCount = tk.Label(topInfoFrame, text='Antal på lager: ', width=int(300*self.scale), justify=tk.LEFT)
        self.lblBookCount.pack(side=tk.BOTTOM)
        self.lblBookPrice = tk.Label(topInfoFrame, text='Pris: ', width=int(300*self.scale), justify=tk.LEFT)
        self.lblBookPrice.pack(side=tk.BOTTOM)
        self.lblBookTitle = tk.Label(topInfoFrame, text='Titel: ', width=int(300*self.scale), justify=tk.LEFT)
        self.lblBookTitle.pack(side=tk.BOTTOM)
        self.butPurchase = tk.Button(topInfoFrame, text='Bestil flere', width =int(70*self.scale), command=self.purchase_current)
        self.butPurchase.pack(side=tk.BOTTOM)
        
        self.update_book_list(None)
    
    def purchase_current(self):
        def confirm_purchase():
            #Get the amount to purchase
            n = int(s.get())
            #Add the items to the stock
            salesItem.stockCount += n
            #Make a transaction to subtract the price
            t = self.get_transaction(Transaction.STOCK_PURCHASE)
            
            t.amount = n * salesItem.price
            t.state = Transaction.ST_READY
            
            #Update the GUI
            
            self.show_book_info(None)
            self.update_economy()
            
            #Close the dialog
            dlg.destroy()
        
        sel = self.lbBooks.curselection()
        if len(sel) > 0:
            salesItem = self.stock.find_sales_item(self.lbBooks.get(sel[0])[1])
            if salesItem is not None:
                dlg = tk.Toplevel(height=200, width=200)
                dlg.title('Bestil bøger')
                b = tk.Button(dlg, text='OK', command=confirm_purchase)
                b.pack(side=tk.BOTTOM)
                s = tk.Spinbox(dlg, text='Antal', from_=0, to=10)
                s.pack(side=tk.BOTTOM)
                e = tk.Label(dlg, text='Bestil eksemplarer af: ' + salesItem.name)
                e.pack(side=tk.BOTTOM)
                dlg.mainloop()
        
    
    def log_message(self, message):
        self.console.insert(tk.END, message)
        self.console.see('end')
   
    def show_employees(self):
        dlg = tk.Toplevel(height=200, width=400)
        dlg.title('Ansatte')
        lbl = tk.Label(dlg, text='Endnu ikke implementeret', width=int(200*self.scale))
        lbl.pack()
        b = tk.Button(dlg, text='OK', command=dlg.destroy)
        b.pack()
        dlg.mainloop()
    
    def add_employee(self):
        def confirm():
            name = nameEntry.get()
            if name == '':
                return self.error('Navn er ikke intastet')
            if any(char.isdigit() for char in name):
                return self.error('Ikke et validt navn')
                
            salery = saleryEntry.get()
            if salery == '':
                return self.error('Løn er ikke intastet')
            
            try:
                salery = float(salery)
            except ValueError:
                return self.error('Løn er ikke en talværdi')
            
            if salery < 0:
                return self.error('Løn må ikke være mindre end 0')
            
            employee = Employee(name, salery)
            
            self.employees.append(employee)
            print(employee)
            dlg.destroy()
        
        
        dlg = tk.Toplevel()
        dlg.grid()
        dlg.title('Tilføj ansatte')
        nameLbl = tk.Label(dlg, text='Navn: ')
        nameLbl.grid(row=1, column=1)
        nameEntry = tk.Entry(dlg)
        nameEntry.grid(row=1, column=2)
        saleryLbl = tk.Label(dlg, text='Løn: ')
        saleryLbl.grid(row=2, column=1)
        saleryEntry = tk.Entry(dlg)
        saleryEntry.insert(0, '0')
        saleryEntry.grid(row=2, column=2)
        addBtn = tk.Button(dlg, text='Tilføj', command=confirm)
        addBtn.grid(row=3, column=2)
        
    def error(self, message):
        dlg = tk.Toplevel()
        msgLbl = tk.Label(dlg, text=message)
        msgLbl.pack()
        okBtn = tk.Button(dlg, text='OK', command=dlg.destroy)
        okBtn.pack(side = tk.BOTTOM)
    
    def show_book_info(self, evt):
        sel = self.lbBooks.curselection()
        if len(sel) > 0:
            salesItem = self.stock.find_sales_item(self.lbBooks.get(sel[0])[1])
            self.lblBookTitle.config(text='Titel: ' + salesItem.name)
            self.lblBookPrice.config(text='Pris: {}'.format(salesItem.price))
            self.lblBookCount.config(text='Antal på lager: {}'.format(salesItem.stockCount))
            self.lblBookSales.config(text='Antal solgt: {}'.format(salesItem.sales))
            #self.lblBookSales.config(text='Antal solgte: {}'.format(salesItem.sales))

    def update_book_list(self, evt):
        sel = self.lbCategories.curselection()
        if len(sel) > 0:
            group = self.lbCategories.get(sel[0])
            titles = self.stock.get_item_list(group)
            self.lbBooks.delete(0,tk.END)
            for t in titles:
                self.lbBooks.insert(tk.END, t)
                
                
app = Boghandelen()

app.master.title('Boghandelen')

app.mainloop()