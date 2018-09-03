# -*- coding: utf-8 -*-
class Employee:
    
    #Counter for employee id factory
    ID_COUNT = 0
    
    def __init__(self, name, salary):
        self.paychecks = []
        self.name = name
        self.salary = salary
        self.employeeId = self.get_next_id()
        
    def total_salary(self):
        totalSalary = 0
        for paycheck in self.paychecks:
            totalSalary += paycheck.amount
        
        return totalSalary
    
    @classmethod    
    def get_next_id(cls):
        cls.ID_COUNT += 1
        return cls.ID_COUNT
    