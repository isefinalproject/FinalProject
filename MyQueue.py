'''
Created on Apr 20, 2017

@author: Trent Insull
'''

class MyQueue():
    def __init__(self):
        self.queue = []
        
    def isEmpty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False
    
    
    def push(self, item):
        self.queue.insert(0,item)
        
    def pop(self):
        return self.queue.pop()
    
    
    
