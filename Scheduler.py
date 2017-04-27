'''
Created on Apr 19, 2017

@author: Trent Insull
'''
from coinor.gimpy import Graph
from coinor.gimpy import DIRECTED_GRAPH as DIRECTED_GRAPH
from Truck import Truck
from Tkconstants import CURRENT


"""
TO DO:
FILTER PATH LIST TO INCLUDE EACH NODE ONCE INSTEAD OF 3 TIMES
DOUBLE CHECK TRUCKS ARE GETTING ROUTED CORRECTLY
VISUALIZE TRUCKS MOVING
IMPLEMENT HEURISTIC?
"""
class Network(Graph):
    
    def __init__(self):
        Graph.__init__(self, graph_type = DIRECTED_GRAPH)
        
    def add_connection(self, name1, name2, label1 = None, label2 = None):
        if self.get_node(name1) is None:
            if label1 is not None:
                self.add_node(name1, label = label1)
            else:
                self.add_node(name1)
        if self.get_node(name2) is None:
            if label2 is not None:
                self.add_node(name2, label = label2)
            else:
                self.add_node(name2)
        # Add if connection does not already exist
        if self.check_edge(name1, name2) is False:
            self.add_edge(name1, name2)
            
    def add_entity(self, name, label = None):
        if label is not None:
            self.add_node(name, label = label)
        else:
            self.add_node(name)

class Scheduler():
    
    
    """
    V - set of vertices, key=ID, value=coordinates
    E - edges (hashtable), key=edge, value="length" in minutes
    Trucks - key=ID, value=Initial Location of a truck
    """
    def __init__(self, V, E, Trucks):
        self.V =  V
        self.E = E
        #CREATE NETWROK
        self.network = Graph(type = DIRECTED_GRAPH)
        #for nodes in the list of vertices add the node to the netwrok
        for node in self.V:
            self.network.add_node(node, label = None)
        #for each edge in edges    
        for edge in self.E:
            #add an edge both ways since graph is directed    
            self.network.add_edge(edge[0],edge[1])
            self.network.add_edge(edge[1],edge[0])
            #add costs to both edges
            self.network.set_edge_attr(edge[0],edge[1], 'cost', self.E[edge])
            self.network.set_edge_attr(edge[1],edge[0], 'cost', self.E[edge])
            
            
        self.Trucks = Trucks
        for truck in self.Trucks:
            val = truck
            key = Trucks[truck]
            self.Trucks[val] = Truck(val, key)
        #get paths from each node to each other node
        self.validity, self.distance, self.nextn = self.paths()
        
    
    def processNewOrders(self, newOrders):
        #for each new order
        truckNum = 0
        
        for order in newOrders:
            
            #get start node
            pickUpPoint = order[0]
            #get end node
            dropOffPoint = order[1]
            if self.distance[(pickUpPoint,dropOffPoint)] == 'infinity' or self.distance[(pickUpPoint,dropOffPoint)] == 0:
                pass
            else:
                #get start node
                pickUpPoint = order[0]
                #get end node
                dropOffPoint = order[1]
                """
                #DOES NOT FIND CLOSEST TRUCK, JUST ASSIGN TO NEXT TRUCK IN LIST
                currLocation = self.Trucks[truckNum].getCurrentLocation()
                self.Trucks[truckNum].location = [currLocation[0],pickUpPoint,0,self.distance[(currLocation[0],pickUpPoint)]]
                self.Trucks[truckNum].queue.push([pickUpPoint,dropOffPoint,0,self.distance[(pickUpPoint,dropOffPoint)]])
                #self.Trucks[truckNum].queue.put([startNode,endNode,0,self.distance[(startNode,endNode)]])
                if truckNum < 133:
                    truckNum += 1
                
                """
                #truckToBeUsed = self.Trucks[0]
                #SAVE FOR LATER
                ###FIND TRUCK CLOSEST TO START NODE
                
                for truck in self.Trucks.values():
                    holderDistance = 1000000000
                    currLocation = truck.getCurrentLocation()
                    #if currently on a node (not in the middle of a delivery)
                    if truck.isTravelling() == False:
                        truckToBeUsed = truck
                        #if distance from trucks current location to start node is less than holder distance
                        if self.distance[(currLocation[0],pickUpPoint)] < holderDistance:
                            #reset holder distance to distance from current node to pickup point
                            holderDistance = self.distance[(currLocation[0],pickUpPoint)]
                            #save what truck this is
                            truckToBeUsed = truck
                #set truck into motion from its current location to the pickup node
                currentPoint = truckToBeUsed.getCurrentLocation()
                if truckToBeUsed.isTravelling() == False and currentPoint[1] == None:
                    
                    startLocation = currentPoint[0]
                    truckToBeUsed.location = [startLocation,pickUpPoint,0,self.distance[(startLocation,pickUpPoint)]]
                    truckToBeUsed.queue.push([pickUpPoint, dropOffPoint,0,self.distance[(pickUpPoint,dropOffPoint)]])
                    truckToBeUsed.travelling = True
                    
                    
                    

                
            

                
                #SAVE FOR LATER WHEN KEEPING TRACK ON EDGE TO EDGE
                #create array of nodes on path from start to end
                #pathForTruck = self.network.floyd_warshall_get_path(self.distance,self.nextn, pickUpPoint, dropOffPoint)
                #print pathForTruck
                # for each two sets of nodes on the path
                #truckToBeUsed.queue.push([pathForTruck[0],pathForTruck[len(pathForTruck)-1],0,self.distance[pathForTruck[0],pathForTruck[len(pathForTruck)-1]]])
                """
                for i in range(0, len(pathForTruck)-1):
                    #append that node, the next node, 0 total distance travel, and distance between nodesto be travelled on
                    #if i < (len(pathForTruck)):
                    truckToBeUsed.queue.push([pathForTruck[i],pathForTruck[i+1],0,self.distance[pathForTruck[i],pathForTruck[i+1]]])
                    #print [pathForTruck[i],pathForTruck[i+1],0,self.distance[pathForTruck[i],pathForTruck[i+1]]]
                    i+=10000000000000
                """  
                    
                
              
                

            

    
    
    
    def updateLocationOfTrucks(self):
        #for each truck
        for truck in self.Trucks.values():
            #set location to current location
            truck.updateLocation()
    
    """
    use gimpy provided solutions as stated in class
    """
    def paths(self, first = None, second = None, path = []):

        #calls floyd warshall algo on graph, retrieves true/false if graph contains negative cycle
        #distance is a dictionary of shortest distances between nodes
        #nextn is dictionary that helps retrieve shortest path between nodes
        validity, distance, nextn = self.network.floyd_warshall()
        return validity, distance, nextn

    
    """
    for each truck create a file  history_truckId.log
    which will save the travel history of each truck (also those which you haven't used)
    """
    def saveTravelHistoryOfAllTrucks(self):
        
        
        pass
    
    def printHistoriesOfAllTrucks(self):
        totalMilesDriven = 0
        
        for truck in self.Trucks.values():
            print truck.getTotalTravelHistory()
            #for i in truck.getTotalTravelHistory():
                #totalMilesDriven += i[3]
        print "Your fleet drove a total of " + str(totalMilesDriven) + " miles"