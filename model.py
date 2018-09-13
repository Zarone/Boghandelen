# -*- coding: utf-8 -*-
import tkinter as tk
from stock import Stock
from transaction import Transaction
from employee import Employee
from fpdf import FPDF

class Model():
    def __init__(self):
        
        self.accounting = []
        
        self.stock = Stock()
        self.stock.build_initial_stock()

        self.markup = tk.DoubleVar()
        self.markup.set(1.3)
        
        self.employees = []
        #Add two initial employees
        e1 = Employee("John", 500)
        self.employees.append(e1)
        e2 = Employee("Jane", 500)
        self.employees.append(e2)

        self.activate_auto_restock = tk.IntVar()

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

    def add_employee(self, name, salary):
        employee = Employee(name, salary)
        self.employees.append(employee)
    
    def update_employee(self, id, salary):
        employee = self.get_employee_by_id(id)
        assert employee is not None
        if employee != None:
            employee.salary = salary
    
    def get_employee_by_id(self, employeeId):
        for employee in self.employees:
            if employee.employeeId == employeeId:
                return employee
        return None
    
    def export_transactions(self):
        pdf = FPDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        for i, trans in enumerate(self.accounting):
            
            output = 'Id: ' + str(trans.transactionId) + ' | Type: ' + str(trans.get_type()) + ' | Beløb: ' + str(trans.amount)
            pdf.cell(1,10, output, 0, 1)
        pdf.output('transaktioner.pdf')
    
    
