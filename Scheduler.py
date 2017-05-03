'''
Created on Apr 19, 2017
@author: Trent Insull
'''
from coinor.gimpy import Graph
from coinor.gimpy import DIRECTED_GRAPH as DIRECTED_GRAPH
from Truck import Truck

import pygame



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
        #initialize pygame
        pygame.init()
        #set framerate
        self.framerate = 15
        #set screen dimension to space out nodes
        screenDimension = [1200,640] 
        #load truck image
        self.truckPic1 = pygame.image.load('truck.png')
        #scale picture down
        self.truckPic = pygame.transform.scale(self.truckPic1, (20, 20))
        #display screen
        self.screen = pygame.display.set_mode(screenDimension)
        self.screen.fill((255,255,255))

        #pygame.draw.rect(self.background, (0,0,0), (0,0, self.screenDimension[0],self.screenDimension[1]))
        self.clock = pygame.time.Clock()
        #initalize cities dictionary
        self.cities = {}
        #get nodes
        self.V =  V
        #get edges
        self.E = E
        #set max x and y to unrealistically low numbers
        maxy = 0
        maxx = 0
        #set min x and y to unrealistically high numbers
        minx = 100000000000
        miny = 100000000000
        #for each node, if x/y coordinate is >/< max/min x/y, reset max or min x,y
        for node in V:
            if V[node][1] >  maxy:
                maxy = V[node][1]
            elif V[node][1] < miny:
                miny = V[node][1]
            if V[node][0] >  maxx:
                maxx = V[node][0]
            elif V[node][0] < minx:
                minx = V[node][0]
        
        #print maxx, minx
        #print maxy, miny
        #set scale of nodes so they all fit well on screen, doesn't change distances
        self.scale = [(screenDimension[0]-300)/((maxx-minx)), (screenDimension[1]-300)/((maxy-miny)/2)]
        
        #CREATE NETWORK
        self.network = Graph(type = DIRECTED_GRAPH)
        #for nodes in the list of vertices add the node to the network
        for node in self.V:
            self.network.add_node(node)
            #set coordinates of cities to integers scaled
            self.cities[node] = [int((V[node][0]-minx)*self.scale[0])+15, int((V[node][1]-miny)*self.scale[1])+15]
            #print self.cities[node]
            #if x coord is over a certain amount scale y a bit so that nodes are more spread out
            if self.cities[node][0] > 700:
                self.cities[node][1] = int((V[node][1]-miny)*1.5*self.scale[1])+15
            #for certain nodes, scaled onto screen, doesn't change distances
            if self.cities[node] == [15,15]:
                self.cities[node] = [400, 100]
            if self.cities[node] == [417,695]:
                self.cities[node] = [407, 400]
            if self.cities[node] == [462,659]:
                self.cities[node] = [452, 400]
            #print self.cities[node]
            #self.cities[node] = (int((V[node][0])/10000), int((V[node][1])/10000))
        #for each node in cities dictionary, draw on map
        for node in self.cities:
            pygame.draw.circle(self.screen, (255,0,0), self.cities[node], 1, 0)
            
        #for each edge in edges    
        for edge in self.E:
            #add an edge both ways since graph is directed    
            self.network.add_edge(edge[0],edge[1])
            self.network.set_edge_attr(edge[0],edge[1], 'cost', self.E[edge])
            #draw edge on map
            pygame.draw.lines(self.screen, (0,128,0), False, [self.cities[edge[0]], self.cities[edge[1]]], 1)
            #add costs to both edges
            self.network.add_edge(edge[1],edge[0])
            self.network.set_edge_attr(edge[1],edge[0], 'cost', self.E[edge])
        #update display
        pygame.display.flip()
           
        
        self.Trucks = Trucks
        #for each truck in trucks, create it as a truck object
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
            #if order is infeasible, throw it out
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
                    #set holder distance unrealistically high
                    holderDistance = 1000000000
                    #get current location of truck
                    currLocation = truck.getCurrentLocation()
                    #if truck is not travelling
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
                    
                    #try to create array of nodes on path from start to end, else pass
                    #pathForTruck = self.network.floyd_warshall_get_path(self.distance,self.nextn, pickUpPoint, dropOffPoint)
                    #print pathForTruck
                    try:
                        path1 = self.network.floyd_warshall_get_path(self.distance, self.nextn, startLocation, pickUpPoint)
                    except:
                        print "nodes not connected"
                        pass
                    #get final path from start location to pickup point
                    finalPath1 = self.fixPath(path1, self.distance)
                    #print path1
                    #print finalPath1
                    #get path from pick up point to drop off point
                    path2 = self.network.floyd_warshall_get_path(self.distance, self.nextn, pickUpPoint, dropOffPoint)
                    #fix path
                    finalPath2 = self.fixPath(path2, self.distance)
                    #print finalPath2
                    
                    truckToBeUsed.updateHistory("ROUTE TO PICKUP")
                    #For the paths, push sequences to queues
                    for i in xrange(len(finalPath1)):
                        truckToBeUsed.queue.push(finalPath1[i])
                        #print "pushed"
                    for i in xrange(len(finalPath2)):
                        truckToBeUsed.queue.push(finalPath2[i])
                        
                     
                        

                    
                    #set truck travelling to true
                    truckToBeUsed.travelling = True



            

    def fixPath(self, path, distance):
        #create empty arrays
        fixedPath = []
        noRepeatPath = []
        #for each node in the path
        for i in xrange(len(path)):
            #if its not already in the no repeat array, add it
            if path[i] not in noRepeatPath:
                noRepeatPath.append(path[i])
        #for each node in no repeat array, add it in correct format
        for i in xrange(len(noRepeatPath)-1):
            fixedPath.append([noRepeatPath[i], noRepeatPath[i+1], 0, distance[noRepeatPath[i], noRepeatPath[i+1]]])
            
        return fixedPath
        
    
    
    
    def updateLocationOfTrucks(self):
        #reset screen
        pygame.draw.rect(self.screen, (255,255,255), (0,0, 1200,640))
        #for each truck
        for truck in self.Trucks.values():
            #set location to current location
            truck.updateLocation()
            #self.displayTrucks(truck)
            #get current location of truck
            location = truck.getCurrentLocation()
            #if currently moving
            if location[1] != None:
                #if X2 < X1
                if self.cities[location[1]][0] < self.cities[location[0]][0]:
                    #if Y2 < Y1, go negative x and negative y
                    if self.cities[location[1]][1] < self.cities[location[0]][1]:
                        truckx = self.cities[location[0]][0] - abs((location[2]/location[3])*(self.cities[location[1]][0]-self.cities[location[0]][0]))
                        trucky =  self.cities[location[0]][1] - abs((location[2]/location[3])*(self.cities[location[1]][1]-self.cities[location[0]][1]))
                        #pygame.draw.rect(self.screen, (255,0,0),(truckx,trucky,8,5), 0)
                        self.screen.blit(self.truckPic, (truckx,trucky))
                    #if Y1 > Y2, go negative x and positive y
                    if self.cities[location[1]][1] > self.cities[location[0]][1]:
                        truckx = self.cities[location[0]][0] - abs((location[2]/location[3])*(self.cities[location[1]][0]-self.cities[location[0]][0]))
                        trucky = self.cities[location[0]][1] + abs((location[2]/location[3])*(self.cities[location[1]][1]-self.cities[location[0]][1]))
                        #pygame.draw.rect(self.screen, (255,0,0),(truckx,trucky,8,5), 0)
                        self.screen.blit(self.truckPic, (truckx,trucky))
                #else if X1 > X2
                else:
                    # If Y2 < Y1 go positive x and negative y
                    if self.cities[location[1]][1] < self.cities[location[0]][1]:
                        truckx = self.cities[location[0]][0] + abs((location[2]/location[3])*(self.cities[location[1]][0]-self.cities[location[0]][0]))
                        trucky =  self.cities[location[0]][1] - abs((location[2]/location[3])*(self.cities[location[1]][1]-self.cities[location[0]][1]))
                        #pygame.draw.rect(self.screen, (255,0,0),(truckx,trucky,8,5), 0)
                        self.screen.blit(self.truckPic, (truckx,trucky))
                        
                    # If Y2 > Y1, go positive x and positive y  
                    if self.cities[location[1]][1] > self.cities[location[0]][1]:
                        truckx = self.cities[location[0]][0] + abs((location[2]/location[3])*(self.cities[location[1]][0]-self.cities[location[0]][0]))
                        trucky = self.cities[location[0]][1] + abs((location[2]/location[3])*(self.cities[location[1]][1]-self.cities[location[0]][1]))
                        #pygame.draw.rect(self.screen, (255,0,0),(truckx,trucky,8,5), 0)
                        self.screen.blit(self.truckPic, (truckx,trucky))
        #for node in cities, draw on map
        for node in self.cities:
            pygame.draw.circle(self.screen, (255,0,0), self.cities[node], 3, 0)
        #for edge in edges, draw on map
        for edge in self.E:
            pygame.draw.lines(self.screen, (0,128,0), False, [self.cities[edge[0]], self.cities[edge[1]]], 1)
        
        #for truck in self.Trucks:
        #tick clock
        self.clock.tick(self.framerate)
        #update display
        pygame.display.flip()
        

        
    
         
        
        
        
        
        

    def finishPygame(self):
        #close pygame
        pygame.display.quit()
        pygame.quit()
    
    
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
        #for each truck
        for truck in self.Trucks.values():
            #get its travel history
            truckHistory = truck.getTotalTravelHistory()
            #write it to its log file
            f = open('history_'+str(truck.id)+'.log.txt', 'w')
            f.write(str(truckHistory))
            f.close()
        
        
    
    def printHistoriesOfAllTrucks(self):
        
        totalMinutesDriven = 0
        #for each truck
        for truck in self.Trucks.values():
            #print total history
            print truck.getTotalTravelHistory()
            #sum all minutes driven
            for i in truck.getTotalTravelHistory():
                #check to make sure not a string instance
                if not isinstance(i, basestring):
                    totalMinutesDriven += i[3]
        print "Your fleet drove a total of " + str(totalMinutesDriven) + " minutes"