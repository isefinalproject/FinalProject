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
        
    
    def processNewOrders(self, newOrders):
        trucknum = 0
        #for each order in incoming orders
        for order in newOrders:
            self.updatequeue(self.paths(self.Trucks[trucknum],newOrders[order][0]))
            self.updatequeue(self.paths(newOrders[order][0], newOrders[order][1]))
            trucknum += 1
            
        """
        Psuedo code for this section
        For each order in new orders:
            Find the truck that can drive to the pickup point to pickup package and then dropoff in shortest distance
            Assign that truck the order
            Update trucks history accordingly
            update that trucks location
        """
    
    
    
    def updateLocationOfTrucks(self):
        #for each truck
        for truck in self.Trucks:
            #set location to current location
            truck.updateLocation(self.Trucks[truck])
    
    """
    use gimpy provided solutions as stated in class
    """
    def paths(self, first, second, path = []):
        
        """
        OLD CODE
        
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
        #call gimpy search method
        return Graph.search(first, second, algo = 'dijkstra')
    
    """
    for each truck create a file  history_truckId.log
    which will save the travel history of each truck (also those which you haven't used)
    """
    def saveTravelHistoryOfAllTrucks(self):
        
        
        pass
    
    