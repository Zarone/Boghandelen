# -*- coding: utf-8 -*-
class Employee:
    
    #Counter for employee id factory
    ID_COUNT = 0
    
    def __init__(self, name, salary):
        self.paychecks = []
        self.name = name
        self.salary = salary
        self.employeeId = self.get_next_id()
        
    def __str__(self):
        totalSalary = 0
        for paycheck in self.paychecks:
            totalSalary += paycheck.amount
        
        return 'Id: ' + str(self.employeeId) + '\nNavn: ' + self.name + '\nLøn: ' + str(self.salary) + '\nUdbetalt ialt: ' + str(totalSalary)
        
    @classmethod    
    def get_next_id(cls):
        cls.ID_COUNT += 1
        return cls.ID_COUNT
    