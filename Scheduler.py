'''
Created on Apr 14, 2017

@author: Trent Insull
'''

from coinor.gimpy import Graph 

from Truck import Truck

class Scheduler:
    
    
    """
    V - set of vertices, key=ID, value=coordinates
    E - edges (hashtable), key=edge, value="length" in minutes
    Trucks - key=ID, value=Initial Location of a truck
    """
    def __init__(self, V, E, Trucks):
        self.V = V
        self.E = E
        self.Trucks = Trucks
        
        
        
        pass
    
    
    def processNewOrders(self, newOrders):
        #from A-> B
        location = [A,B]
        
        
        pass 
    
    
    
    def updateLocationOfTrucks(self, V, E, Truck):
        for truck in self.Trucks:
            truck.updateLocation(location);
        pass
    
    
    """
    for each truck create a file  history_truckId.log
    which will save the travel history of each truck (also those which you haven't used)
    """
    def saveTravelHistoryOfAllTrucks(self):
        
        
        pass