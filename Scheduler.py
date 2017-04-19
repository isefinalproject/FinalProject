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
        #get paths from each node to each other node
        self.validity, self.distance, self.nextn = self.paths()
        
    
    def processNewOrders(self, newOrders):
        """ OLD CODE
        trucknum = 0
        #for each order in incoming orders
        for order in newOrders:
            self.updatequeue(self.paths(self.Trucks[trucknum],newOrders[order][0]))
            self.updatequeue(self.paths(newOrders[order][0], newOrders[order][1]))
            trucknum += 1
        """
        #for each new order
        for order in newOrders:
            #get start node
            startNode = newOrders[order][0]
            #get end node
            endNode = newOrders[order][1]
            ###FIND TRUCK CLOSEST TO START NODE
            holderDistance = 1000000000
            for truck in self.Trucks:
                currLocation = truck.getCurrentLocation()
                #if current on a node
                if currLocation[1] == None:
                    if self.distance[(currLocation,startNode)] < holderDistance:
                        holderDistance = self.distance[(currLocation,startNode)]
                        truckToBeUsed = truck
                #else if on an arc
                else:
                    #COMPUTE DISTANCE
                    truckToBeUsed = truck 
            ###ASSIGN THE TRUCK THE ROUTE FROM ITS CURRENT LOCATION TO START NODE TO END NDOE
            truckToBeUsed.queue.append([order[0],order[1],0,self.distance[(order[0],order[1])]])
            ###UPDATE TRUCK HISTORY
            
            ###UPDATE LOCATIONS
            
            
            
            
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
    def paths(self, first = None, second = None, path = []):
        
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
        #calls floyd warshall algo on graph, retrieves true/false if graph contains negative cycle
        #distance is a dictionary of shortest distances between nodes
        #nextn is dictionary that helps retrieve shortest path between nodes
        validity, distance, nextn = Graph.floyd_warshall()
        return validity, distance, nextn
        #rturn nextn?
        
        #call gimpy search method
        #return Graph.search(first, second, algo = 'dijkstra')
    
    """
    for each truck create a file  history_truckId.log
    which will save the travel history of each truck (also those which you haven't used)
    """
    def saveTravelHistoryOfAllTrucks(self):
        
        
        pass
    
    