'''
Created on Apr 19, 2017

@author: Trent Insull
'''
from coinor.gimpy import Graph
from coinor.gimpy import DIRECTED_GRAPH as DIRECTED_GRAPH
from Truck import Truck
from Tkconstants import CURRENT
import pygame


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
        pygame.init()
        self.framerate = 10
        screenDimension = (740,580) 
        self.screen = pygame.display.set_mode(screenDimension)
        self.screen.fill((255,255,255))
        pygame.display.set_caption("Awesome team")
        background = self.screen.convert()
        self.clock = pygame.time.Clock()
        
        self.cities = {}
        self.V =  V
        self.E = E
        #CREATE NETWROK
        self.network = Graph(type = DIRECTED_GRAPH)
        #for nodes in the list of vertices add the node to the netwrok
        for node in self.V:
            self.network.add_node(node)
            self.cities[node] = (int(V[node][0]*10), int(V[node][1]*10))
            
        for node in self.cities:
            pygame.draw.circle(self.screen, (50,100,150), self.cities[node], 8, 0)
        #for each edge in edges    
        for edge in self.E:
            #add an edge both ways since graph is directed    
            self.network.add_edge(edge[0],edge[1])
            self.network.set_edge_attr(edge[0],edge[1], 'cost', self.E[edge])
            pygame.draw.lines(self.screen, (0,0,0), False, [self.cities[edge[0]], self.cities[edge[1]]], 1)
            #add costs to both edges
            self.network.add_edge(edge[1],edge[0])
            self.network.set_edge_attr(edge[1],edge[0], 'cost', self.E[edge])
        pygame.display.update()
        #pygame.display.flip()
        #self.display()    
            
        self.Trucks = Trucks
        for truck in self.Trucks:
            val = truck
            key = Trucks[truck]
            self.Trucks[val] = Truck(val, key)
        #get paths from each node to each other node
        self.validity, self.distance, self.nextn = self.paths()
        
    
    def processNewOrders(self, newOrders):

        
        for order in newOrders:
            
            #get start node
            pickUpPoint = order[0]
            #get end node
            dropOffPoint = order[1]
            if self.distance[(pickUpPoint,dropOffPoint)] == 'infinity' or self.distance[(pickUpPoint,dropOffPoint)] == 0 or pickUpPoint == None:
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
                
                ###FIND TRUCK CLOSEST TO START NODE
                #pathForTruck = self.network.floyd_warshall_get_path(self.distance,self.nextn, pickUpPoint, dropOffPoint)
                for truck in self.Trucks.values():
                    holderDistance = 1000000000
                    currLocation = truck.getCurrentLocation()
                    #if currently on a node (not in the middle of a delivery)
                    #print truck.isTravelling()
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
                if truckToBeUsed.isTravelling() == False and (currentPoint[0], pickUpPoint) in self.distance:
                    
                    startLocation = currentPoint[0]
                    #truckToBeUsed.updateHistory("ROUTE TO PICKUP")
                    #truckToBeUsed.location = [startLocation,pickUpPoint,0,self.distance[(startLocation,pickUpPoint)]]
                    #truckToBeUsed.queue.push([pickUpPoint, dropOffPoint,0,self.distance[(pickUpPoint,dropOffPoint)]])
                    
                    #create array of nodes on path from start to end
                    #pathForTruck = self.network.floyd_warshall_get_path(self.distance,self.nextn, pickUpPoint, dropOffPoint)
                    #print pathForTruck
                    try:
                        path1 = self.network.floyd_warshall_get_path(self.distance, self.nextn, startLocation, pickUpPoint)
                    except:
                        print "nodes not connected"
                        pass
                    finalPath1 = self.fixPath(path1, self.distance)
                    #print path1
                    #print finalPath1
                    path2 = self.network.floyd_warshall_get_path(self.distance, self.nextn, pickUpPoint, dropOffPoint)
                    finalPath2 = self.fixPath(path2, self.distance)
                    #print finalPath2
                    
                    for i in xrange(len(finalPath1)):
                        truckToBeUsed.queue.push(finalPath1[i])
                        #print "pushed"
                    for i in xrange(len(finalPath2)):
                        truckToBeUsed.queue.push(finalPath2[i])
                        
                     
                        

                    
                
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
                    
                
              
                

            

    def fixPath(self, path, distance):
        fixedPath = []
        noRepeatPath = []
        for i in xrange(len(path)):
            if path[i] not in noRepeatPath:
                noRepeatPath.append(path[i])
        for i in xrange(len(noRepeatPath)-1):
            fixedPath.append([noRepeatPath[i], noRepeatPath[i+1], 0, distance[noRepeatPath[i], noRepeatPath[i+1]]])
            
        return fixedPath
        
    
    
    
    def updateLocationOfTrucks(self):
        #for each truck
        for truck in self.Trucks.values():
            #set location to current location
            truck.updateLocation()
        for node in self.cities:
            pygame.draw.circle(self.screen, (50,100,150), self.cities[node], 8, 0)
        for edge in self.E:
            pygame.draw.lines(self.screen, (0,0,0), False, [self.cities[edge[0]], self.cities[edge[1]]], 1)
        self.clock.tick(self.framerate)
        pygame.display.update()
        print 'hi'

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