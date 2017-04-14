from coinor.gimpy import Graph

class Scheduler:
    
    
    """
    V - set of vertices, key=ID, value=coordinates
    E - edges (hashtable), key=edge, value="length" in minutes
    Trucks - key=ID, value=Initial Location of a truck
    """
    def __init__(self, V, E, Trucks):
        self.V =  V
        self.E = E
        self.Trucks = Trucks
        pass
    
    def processNewOrders(self, newOrders):
        trucknum = 0
        for order in newOrders:
            self.updatequeue(self.paths(self.Trucks[trucknum],newOrders[order][0]))
            self.updatequeue(self.paths(newOrders[order][0], newOrders[order][1]))
            trucknum += 1
    
    
    
    def updateLocationOfTrucks(self):
        for truck in self.Trucks:
            truck.updateLocation(self.Trucks[truck])
    
    
    def paths(self, first, second, path = []):
        path = path + [first]
        if first == second:
            return path
        shortest =  []
        for node in self.get_neighbors(first):
            if node not in path:
                newpath = self.paths(node,second, path)
                if newpath:
                    if not shortest or len(newpath)<len(shortest):
                        shortest = newpath
        return shortest
    
    """
    for each truck create a file  history_truckId.log
    which will save the travel history of each truck (also those which you haven't used)
    """
    def saveTravelHistoryOfAllTrucks(self):
        
        
        pass
    
    