'''
Created on Apr 19, 2017

@author: Trent Insull
'''
from MyQueue import MyQueue
class Truck:
    
    
    def __init__(self, _id, initialLocation):
        self.id = _id
        self.location = [initialLocation, None, 0,0]
        #set initial history array for each truck
        self.history = [[initialLocation, None, 0,0]]
        #queue to handle big order
        self.queue = MyQueue()
        
        
        
        
    """
    Current location of a truck should be either at Node or on a "directed" edge
    together with the information how far on this edge the truck is.
    """    
    def updateLocation(self):
        #if truck is on an arc, increase how far it has gone
        if self.location[2] < self.location[3]:
            self.location[2] += 1
        #if we have reached the node we are on our way to and truck has been driving
        elif self.location[2] == self.location[3] and self.location[3] != 0:
            #update history
            self.updateHistory(self.location)
            #if queue is not empty
            if self.queue.isEmpty() == False:
                self.location = self.queue.pop()
            #else if queue is empty, set truck to rest in its current node
            if self.location[1] != None:
                self.location = [self.location[1], None, 0, 0]
        #if queue is empty stay in current location
        else:
            self.location = self.location
        
        
         
    
        """
    it should return the edge and also how far he is on this edge, e.g. [A,C],[5,30] 
         if he is traveling 5 minutes on an edge A->C which takes 30 minutes to travel 
    """
    def getCurrentLocation(self):
        return self.location
    """
        Method to add an event to the history log
    """
    def updateHistory(self, input):
        self.history.append(input)
     

        
    """
    This should return total travel history, e.g.
    A,C,30/30,P20;P94;P101    # this means he moved from A to C which was 30 minutes out of 30 minutes, he picked up 3 packages
    C,D,30/40    # then he was traveling from C to D, only for 30 minutes (so he did not get to D)
    D,C,30/40,P33;P34    # then he turn around and went back to C for 30 minutes and picked up 2 packages
    C,E,50/50,D33;D20    # then he went to E and drop package 33 and 20
    """
    def getTotalTravelHistory(self):    
        return self.history