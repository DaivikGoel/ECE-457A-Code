#Depth First Search
from maze1blackspots import blackspots
import numpy as np
import pandas

#any dependencies can be install using pip3 install pandas
#To run just do python3 q6bfs.py

class Node():
    def __init__(self, coord, parent = None):
        #node class holding the coordinate and the parent Node
            self.coord = coord
            self.parent = parent

#visited will contain all the black spots in the maze. Will be in tuple form
#startingcoord and endingcoord will a tuple

def DepthFirstSearch (startingcoord,endingcoord, visited, nodesexplored):
    NodeStack = []
    #holds queue of positions to check
    StartingNode = Node(startingcoord)
    NodeStack.append(StartingNode)
    #add the starting coordinates to the queue

    while(len(NodeStack) != 0):
        #keep going till every point is checked
        currNode = NodeStack.pop()
        if currNode.coord[0] < 0 or currNode.coord[0] >= 25 or currNode.coord[1] < 0 or currNode.coord[1] >= 25 or currNode.coord in visited:
            #if not in maze disregard
            pass
        elif currNode.coord == endingcoord:
            #if we make it to ending coord stop, return the cheapest path and the distance it would take to get there
            nodesexplored += 1
            path = []
            mindistance = 0
            path,mindistance = cheapestpath(currNode, startingcoord, path, mindistance)
            return nodesexplored, path, mindistance
        else:
            if currNode.coord not in visited:
                #make sure coord not already visited. If not add to the the visited queue and one more to nodes explored.
                visited.append(currNode.coord)
                nodesexplored += 1

                for x in [(0,1),(1,0),(-1,0), (0,-1)]:
                    #add neighbours to the queue
                    newcoord = (currNode.coord[0] + x[0],currNode.coord[1] + x[1])

                    if newcoord not in visited:
                        #make sure neighbours arent black spots or already visited
                        NewNode = Node(newcoord, currNode)
                        #adds new nodes to top of queue. Adds current node as parent
                        NodeStack.append(NewNode)
                        
def cheapestpath(Node, startingcoord, path, mindistance):
    #once we find the ending node we can work backwards to find the cheapest path to the first node
    mindistance += 1
    path.insert(0, Node.coord)
    if Node.coord != startingcoord:
        return cheapestpath(Node.parent, startingcoord, path, mindistance)
    else:
        return path, mindistance

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
nodesexplored, path, mindistance = DepthFirstSearch(Origin, TopRight, blacksquares, 0) # (From, To, Maze)
print("NODES EXPLORED:", nodesexplored)
print("PATH", path)
print("MIN DISTANCE:", mindistance)
printgrid(path, S, E1, blackspots)