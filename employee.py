# -*- coding: utf-8 -*-
class Employee:
    
    #Counter for employee id factory
    ID_COUNT = 0
    
    def __init__(self, name, salary):
        self.paychecks = []
        self.name = name
        self.salary = salary
        self.employeeId = self.get_next_id()
        
    @classmethod    
    def get_next_id(cls):
        cls.ID_COUNT += 1
        return cls.ID_COUNT
    