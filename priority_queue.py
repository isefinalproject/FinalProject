'''
Created on Apr 19, 2017

@author: Trent Insull
'''
from platform import node
'''
Created on April 1, 2014

@author: Ted Ralphs
'''

#import heapq
import heapq

class PriorityQueue(object):
    def __init__(self, aList = None):
        self.priorityQueue = {}

    def isEmpty(self):
        #if the length is 0, its empty return true
        #else return false
        return len(self.priorityQueue) == 0
        

    def pop(self, key = None):
        #use peek
        key, priority = self.peek()
        self.priorityQueue.pop(key)  
        return key, priority    
            
    
    def peek(self, key = None):
        '''
        Return the lowest priority item. Raise KeyError if empty.
        '''
        if self.isEmpty():
            raise KeyError("empty")
        else:
            holder = 1000000000
            index = None
            for node in self.priorityQueue:
                if self.priorityQueue[node] < holder:
                    holder = self.priorityQueue[node]
                    index = node
            return index, holder
        

    def get_priority(self, key):
        return self.priorityQueue[key]
    
    def push(self, key, priority = 0):
        self.priorityQueue[key] = priority
    
    def remove(self, key):