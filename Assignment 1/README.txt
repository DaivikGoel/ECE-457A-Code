All the files have been named for their respective methods. 

You may have to install numpy and pandas if you do not have it installed using pip install numpy and pip install pandas.

I am using these libraries just to try giving the output as a maze

To run them all you have to do is: python _.py (or it could be python3 _.py depending on your config). 

Ex. python q6bfs.py

To change which points the maze goes from and to you have to go into the file of each one. If you scroll to the bottom you should see the following:

S = (2,11)
E1 = (23,19)
E2 = (2,21)
Origin = (0,0)
TopRight = (24,24)

Choose which points you want to go from and to and place that into the function.

Ex. nodesexplored, path = BreadthFirstSearch(Origin, TopRight, blacksquares) -> (StartingPoint, EndingPoint, Maze)

You should get an output with all info needed