'''
Created on April 1, 2014

@author: Ted Ralphs
'''

class PriorityQueue(object):
    #worked on lab 6 mostly
    def __init__(self, aList = None):
        self.alist = {}
        #self.key = 0
        

    def isEmpty(self):
        return len(self.alist) == 0

    def pop(self, key = None):
        '''
        Remove and return the lowest priority item. Raise KeyError if empty.
        '''
        if self.isEmpty():
            raise KeyError("Pop")
            
        thing = min(self.alist, key = self.alist.get)
        del self.alist[thing]
        return thing
        
        
        
    
    def peek(self, key = None):
        '''
        Return the lowest priority item. Raise KeyError if empty.
        '''
        if self.isEmpty():
            raise KeyError("peek")
        
        return min(self.alist, key = self.alist.get)

    def get_priority(self, key):
        '''
        Get priority of item with the given key. Raise KeyError if key doesn't exist.
        '''
        if key not in self.alist:
            raise KeyError("get prio")
        return self.alist[key]
    
    def push(self, key, priority = 0):
        '''
        Add to the queue or update the priority of an existing task.
        '''
        #print key
        self.alist[key] = priority
        #print self.alist[key]
        
    def remove(self, key):
        '''
        Remove an existing item with given key.  Raise KeyError if not found.
        '''
        if key not in self.alist:
            raise KeyError(" ")
        del self.alist[key]
        
if __name__=='__main__':
        test = PriorityQueue()
        #print test.isEmpty()
        test.push(3,88)
        test.push(5,89)
        test.push(44,90)
        test.push(3,50)
        print test.get_priority(3)
        print test.peek()
        #test.remove(3)
        print test.pop()
        print test.pop()
        #print test.get_priority(3)