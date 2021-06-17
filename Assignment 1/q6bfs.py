#Breadth First Search
#visited will contain all the black spots in the maze. Will be in tuple form
#startingcoord and endingcoord will a tuple

#any dependencies can be install using pip3 install pandas
#To run just do python3 q6bfs.py
from maze1blackspots import blackspots
import numpy as np
import pandas


def BreadthFirstSearch (startingcoord, endingcoord, visited):

    NodeQueue = []
    #holds queue of positions to check
    nodesexplored = 0
    #holds the count of nodes explored
    NodeQueue.append(startingcoord)
    #add the starting coordinates to the queue

    path = []
    #list holding tuples we visited. Will give us the path to the end
    while(len(NodeQueue) != 0):
        #keep going till every point is checked
        coord = NodeQueue.pop(0)
        if coord[0] < 0 or coord[0] >= 25 or coord[1] < 0 or coord[1] >= 25 or coord in visited:
            #if not in maze disregard
            pass
        elif coord == endingcoord:
            #if we make it to ending coord stop and return the amount of nodes explored(cost) and the path
            nodesexplored += 1
            path.append(coord)
            return nodesexplored, path
        else:
            if coord not in visited:
                #make sure coord not already visited. If not add to the the visited queue and one more to nodes explored. Also add to the path
                visited.append(coord)
                path.append(coord)
                nodesexplored += 1

                for x in [(0,1),(1,0),(-1,0),(0,-1)]:
                    #add neighbours to the queue
                    newcoord = (coord[0] + x[0],coord[1] + x[1])

                    if newcoord not in visited:
                        #make sure neighbours arent black spots or already visited
                        NodeQueue.append(newcoord)

def printgrid(path,blackspots):
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

nodesexplored, path = BreadthFirstSearch(Origin, TopRight, blacksquares) # (From, To, Maze)
print("NODES EXPLORED:", nodesexplored)
print("PATH: ", path)
printgrid(path, blackspots)