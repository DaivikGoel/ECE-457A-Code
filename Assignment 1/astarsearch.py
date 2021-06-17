#A Star Search
#visited will contain all the black spots in the maze. Will be in tuple form
#startingcoord and endingcoord will a tuple
from maze1blackspots import blackspots
import numpy as np
import pandas

#any dependencies can be install using pip3 install pandas
#To run just do python3 q6bfs.py

class Node():
    def __init__(self, coord, cost=0):
        #node class holding the coordinate and the parent Node
            self.coord = coord
            self.cost = cost
            
def Astarsearch(startingcoord,endingcoord, visited):

    NodeQueue = []
    #holds queue of positions to check
    nodesexplored = 0
    #holds the count of nodes explored
    StartingNode = Node(startingcoord)
    #creates first node with starting coordinates
    NodeQueue.append(StartingNode)
    #add the starting coordinates to the queue
    path = []
    totalcost = 0
    #list holding coordinates we visited. Will give us the path to the end

    while(len(NodeQueue) != 0):
        #keep going till every point is checked
        currNode = NodeQueue.pop(0)
        if currNode.coord[0] < 0 or currNode.coord[0] >= 25 or currNode.coord[1] < 0 or currNode.coord[1] >= 25 or currNode.coord in visited:
            #if not in maze disregard
            pass
        elif currNode.coord == endingcoord:
            #if we make it to ending coord stop and return the amount of nodes explored(cost) and the path
            nodesexplored += 1
            return nodesexplored, path, totalcost
        else:
            if currNode.coord not in visited:
                #make sure coord not already visited. If not add to the the visited queue and one more to nodes explored. Also add to the path
                visited.append(currNode.coord)
                path.append(currNode.coord)
                nodesexplored += 1
                totalcost += currNode.cost
                for x in [(0,1),(1,0),(-1,0), (0,-1)]:
                    #add neighbours to the queue
                    newcoord = (currNode.coord[0] + x[0],currNode.coord[1] + x[1])
                    if newcoord not in visited:
                        #make sure neighbours arent black spots or already visited

                        #This is our heuristic function. 
                        # I am seeing if the coordinates of the neighbours are in between the starting coordinates and the end. 
                        # If they arent I give a higher cost to the node
                        xranges = (min(startingcoord[0], endingcoord[0]), max(startingcoord[0], endingcoord[0]))
                        yranges = (min(startingcoord[1], endingcoord[1]), max(startingcoord[1], endingcoord[1]))
                        cost = 1
                        if newcoord[0] not in range(xranges[0], xranges[1]):
                            cost +=1 
                        elif  newcoord[1] not in range(yranges[0], yranges[1]):
                            cost +=1
                        #add the node with cost to queue
                        NewNode = Node(newcoord, cost)
                        NodeQueue.append(NewNode)
                        #sort queue based on cost
                        NodeQueue.sort(key=lambda x: x.cost)

def printgrid(path, startingcoord, endingcoord, blackspots):
    grid = np.zeros((25,25))
    nodeno = 0 
    for coord in path:
        grid[coord[1], coord[0]] = nodeno
        nodeno +=1
    for spot in blackspots:
        grid[spot[1], spot[0]] = 999
    df = pandas.DataFrame(grid, columns=range(25), index=range(25))
    print(df.iloc[::-1])

S = (2,11)
E1 = (23,19)
E2 = (2,21)
Origin = (0,0)
TopRight = (24,24)
blacksquares = blackspots.copy()
#For different start and ending points just change the coordinates in the function
nodesexplored, path, totalcost = Astarsearch(Origin, TopRight, blacksquares) # (From, To, Maze)
print("NODES EXPLORED:", nodesexplored)
print("PATH:", path)
print("TOTAL COST:", totalcost)
printgrid(path, S, E2, blackspots)