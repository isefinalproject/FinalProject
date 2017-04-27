'''
Created on Apr 23, 2017

@author: Trent
'''
from MyQueue import MyQueue

queue = MyQueue()

queue.push(4)
queue.push(5)

print queue.isEmpty()
for i in queue:
    print queue[i]