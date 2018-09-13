# -*- coding: utf-8 -*-

class Transaction:
  
    #Class variables for transaction types
    CUSTOMER_PURCHASE = 1
    EMPLOYEE_SALARY = 2
    STOCK_PURCHASE = 3
    CUSTOMER_RETURN = 4
    
    #Transaction states
    ST_WAITING = 0
    ST_READY = 1
    ST_COMPLETE = 2
    
    #Class id counter
    ID_COUNT = 0
    
    def __init__(self, transactionType, amount=0):
        self.transactionType = transactionType
        self.state = self.ST_WAITING
        self.transactionId = self.get_next_id()
        self.amount = amount
    
    def get_type(self):
        if self.transactionType == 1:
            return "CUSTOMER_PURCHASE"
        elif self.transactionType == 2:
            return "EMPLOYEE_SALARY"
        elif self.transactionType == 3:
            return "STOCK_PURCHASE"
        elif self.transactionType == 4:
            return "CUSTOMER_RETURN"
        else:
            return "Invalid type"
    
    @classmethod    
    def get_next_id(cls):
        cls.ID_COUNT += 1
        return cls.ID_COUNT
    
    