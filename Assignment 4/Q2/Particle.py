import numpy as np 
import random

# https://medium.com/analytics-vidhya/implementing-particle-swarm-optimization-pso-algorithm-in-python-9efc2eb179a6
# referenced this article in terms of implementation

class Particle():

    def __init__(self):
        # this generates random coordinates of i and j between -5 and 5
        i = (-1) ** (bool(random.getrandbits(1))) * random.random()*5
        j = (-1) ** (bool(random.getrandbits(1))) * random.random()*5
        self.position = np.array([i,j])

        # decreases with more iterations to the min
        self.best_value = float('inf') 

        # best position so far:
        self.best_position = self.position

        # initial x and y velocity is 0
        self.velocity = np.array([0,0])


    def update_posn(self):
        self.position = self.velocity + self.position

