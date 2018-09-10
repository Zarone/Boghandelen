# -*- coding: utf-8 -*-
import tkinter as tk
from transaction import Transaction
from fpdf import FPDF
from model import Model
from controller import Controller

class View(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()  
        
        self.model = Model()
        self.controller = Controller(self)

        self.scale = float(1)/6
        self.build_GUI()
        self.controller.post_gui()

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
        self.lblMoney = tk.Label(leftFrame, text='Aktuel bundlinje: {}'.format(self.model.get_total_accounting_value()))
        self.lblMoney.pack(fill=tk.X)
        self.lblTotalBookCount = tk.Label(leftFrame, text='Antal bøger på lager: {}'.format(self.model.stock.get_total_item_count()))
        self.lblTotalBookCount.pack(fill=tk.X)
        
        self.slMarkup = tk.Scale(leftFrame, label=None, resolution=0.1, orient=tk.HORIZONTAL, from_=0, to=2, variable=self.model.markup)
        self.slMarkup.pack(fill = tk.X)
        
        restockLbl = tk.Label(leftFrame, text='Auto indkøb')
        restockLbl.pack(fill=tk.X)
        self.autoRestock = tk.Spinbox(leftFrame, from_=1, to=10000)
        self.autoRestock.pack(side=tk.LEFT)    
        
        activateAutoRestock = tk.Checkbutton(leftFrame,command=self.controller.auto_restock,variable=self.model.activate_auto_restock)
        activateAutoRestock.pack(side=tk.RIGHT)
        
        self.console = tk.Text(rightFrame, width=int(430*self.scale))
        self.console.pack()
        
        lbl1 = tk.Label(topLeftFrame, text='Vælg kategori', width=int(70*self.scale), padx=10)
        lbl1.pack(side = tk.LEFT)
        
        self.categories = self.model.stock.get_itemGroup_list()
        
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
        
        self.lblBookAuthor = tk.Label(topInfoFrame, text='Forfatter: ' , width=int(300*self.scale), justify=tk.LEFT)
        self.lblBookAuthor.pack(side=tk.BOTTOM)
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
            t = self.model.get_transaction(Transaction.STOCK_PURCHASE)
            
            t.amount = n * salesItem.price
            t.state = Transaction.ST_READY
            
            #Update the GUI
            self.show_book_info(None)
            self.controller.update_economy()
            
            #Close the dialog
            dlg.destroy()
        
        sel = self.lbBooks.curselection()
        if len(sel) > 0:
            salesItem = self.model.stock.find_sales_item(self.lbBooks.get(sel[0])[1])
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
        
    def error(self, message):
        dlg = tk.Toplevel()
        msgLbl = tk.Label(dlg, text=message)
        msgLbl.pack()
        okBtn = tk.Button(dlg, text='OK', command=dlg.destroy)
        okBtn.pack(side = tk.BOTTOM)
   
    def show_employees(self):
        dlg = tk.Toplevel()
        dlg.title('Ansatte')
        
        employeeList = tk.Listbox(dlg)
        infoLbl = tk.Label(dlg, text='Ingen valgt ansat')
        
        salaryVar = tk.StringVar(dlg)
        
        idLbl = tk.Label(dlg, text='Id')
        idValueLbl = tk.Label(dlg)
        nameLbl = tk.Label(dlg, text='Navn')
        nameValueLbl = tk.Label(dlg)
        salaryLbl = tk.Label(dlg, text='Løn')
        salaryValueEntry = tk.Spinbox(dlg, from_=0, to=40000, textvariable=salaryVar)
        totalSalaryLbl = tk.Label(dlg, text='Udbetalt ialt')
        totalSalaryValueLbl = tk.Label(dlg)
        
        def hide_info():
            infoLbl.grid(row=2,column=1)
            idLbl.grid_forget()
            idValueLbl.grid_forget()
            nameLbl.grid_forget()
            nameValueLbl.grid_forget()
            salaryLbl.grid_forget()
            salaryValueEntry.grid_forget()
            totalSalaryLbl.grid_forget()
            totalSalaryValueLbl.grid_forget()
            
        def update_info():
            sel = employeeList.curselection()
            if len(sel) > 0:
                id = int(employeeList.get(sel[0]).split(':')[0])
                salary = salaryVar.get()
                self.controller.validate_update_employee(dlg, id, salary)
        
        hide_info()
        
        def show_info(env):
            sel = employeeList.curselection()
            if len(sel) > 0:
                id = int(employeeList.get(sel[0]).split(':')[0])
                employee = self.model.get_employee_by_id(id)
                # Kan godt regne med at den altid retunerer en ansat, men tjekker alligevel.
                if employee == None:
                    return self.error('Kunne ikke finde den ansatte')
                
                idValueLbl.config(text=employee.employeeId)
                nameValueLbl.config(text=employee.name)
                salaryVar.set(str(employee.salary))
                totalSalaryValueLbl.config(text=employee.total_salary())
                
                infoLbl.grid_forget()
                idLbl.grid(row=2,column=1)
                idValueLbl.grid(row=2,column=2)
                nameLbl.grid(row=3,column=1)
                nameValueLbl.grid(row=3,column=2)
                salaryLbl.grid(row=4,column=1)
                salaryValueEntry.grid(row=4,column=2)
                totalSalaryLbl.grid(row=5,column=1)
                totalSalaryValueLbl.grid(row=5,column=2)
        
        employeeList.bind('<<ListboxSelect>>', show_info)
        for employee in self.model.employees:
            employeeList.insert(tk.END, str(employee.employeeId) + ':' + employee.name)
        
        employeeList.grid(row=1,column=1,columnspan=2,sticky='N E W')
        okBtn = tk.Button(dlg, text='OK', command=update_info)
        okBtn.grid(row=6,column=1, sticky='W')
        cancelBtn = tk.Button(dlg, text='Fortryd', command=dlg.destroy)
        cancelBtn.grid(row=6,column=2,sticky='E')
        dlg.mainloop()
    
    def add_employee(self):
        def do():
             name, salary = (nameEntry.get(), salaryEntry.get())
             self.controller.validate_new_employee(dlg, name, salary)
        dlg = tk.Toplevel()
        dlg.grid()
        dlg.title('Tilføj ansatte')
        nameLbl = tk.Label(dlg, text='Navn: ')
        nameLbl.grid(row=1, column=1)
        nameEntry = tk.Entry(dlg)
        nameEntry.grid(row=1, column=2)
        salaryLbl = tk.Label(dlg, text='Løn: ')
        salaryLbl.grid(row=2, column=1)
        salaryEntry = tk.Entry(dlg)
        salaryEntry.insert(0, '0')
        salaryEntry.grid(row=2, column=2)
       
        addBtn = tk.Button(dlg, text='Tilføj', command=do)
        addBtn.grid(row=3, column=2)
    
    def show_book_info(self, evt):
        sel = self.lbBooks.curselection()
        if len(sel) > 0:
            salesItem = self.model.stock.find_sales_item(self.lbBooks.get(sel[0])[1])
            self.lblBookTitle.config(text='Titel: ' + salesItem.name)
            self.lblBookPrice.config(text='Pris: {}'.format(salesItem.price))
            self.lblBookCount.config(text='Antal på lager: {}'.format(salesItem.stockCount))
            self.lblBookSales.config(text='Antal solgt: {}'.format(salesItem.sales))
            self.lblBookAuthor.config(text='Forfatter: {}'.format(salesItem.author))

    def update_employee_information(self, evt):
        sel = self.lbCategories.curselection()
        if len(sel) > 0:
            group = self.lbCategories.get(sel[0])
            titles = self.model.stock.get_item_list(group)
            self.lbBooks.delete(0,tk.END)
            for t in titles:
                self.lbBooks.insert(tk.END, t)
                
    def update_book_list(self, evt):
        sel = self.lbCategories.curselection()
        if len(sel) > 0:
            group = self.lbCategories.get(sel[0])
            titles = self.model.stock.get_item_list(group)
            self.lbBooks.delete(0,tk.END)
            for t in titles:
                self.lbBooks.insert(tk.END, t)
                
app = View()

app.master.title('Boghandelen')

app.mainloop()