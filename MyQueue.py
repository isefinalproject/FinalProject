'''
Created on Apr 20, 2017

@author: Trent Insull
'''

class MyQueue():
    def __init__(self):
        self.queue = []
        
    def isEmpty(self):
        return self.queue == []
    
    
    def push(self, item):
        self.queue.insert(0,item)
        
    def pop(self):
        return self.queue.pop()
    
    
    
