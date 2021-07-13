#initial commit

import random
import math
import numpy as np
import matplotlib.pyplot as plt

#cities array
cities = [
    (1, 1150, 1760),(2, 630, 1660),(3, 40, 2090),(4, 750, 1100),(5, 750, 2030),(6, 1030, 2070),(7, 1650, 650),(8, 1490, 1630),(9, 790, 2260),(10, 710, 1310),(11, 840, 550),(12, 1170, 2300),(13, 970, 1340),(14, 510, 700),(15, 750, 900),(16, 1280, 1200),(17, 230, 590),(18, 460, 860),(19, 1040, 950),(20, 590, 1390),(21, 830, 1770),(22, 490, 500),(23, 1840, 1240),(24, 1260, 1500),(25, 1280, 790),(26, 490, 2130),(27, 1460, 1420),(28, 1260, 1910),(29, 360, 1980)
]
#class created for the ant to hold the current city and the travelled cities

class Ant: 

    def __init__(self, source_node):
        self.city = source_node
        self.travelled = [source_node]

def ACO (alpha, beta, base_ph, ant_pop, phermone_decay, state_transition, online_phermone, Q, iter):
    phermones = [[base_ph for x in range(len(cities))] for y in range(len(cities))] 
    cost_per_iteration = []

    for i in range(iter):
        source_node = cities[random.randint(0,28)]
        ants = []


        for x in range(ant_pop):
            ants.append(Ant(source_node))
        best_cost = math.inf
        best_ant = None
        for ant in ants:
            while len(ant.travelled) != len(cities):
                select_next_city(ant, phermones, alpha, beta, state_transition)
            if online_phermone == True:
                online_delayed_update(ant, Q, phermones)
            ant_total_cost = totalcost(ant.travelled)

            best_ant = ant if ant_total_cost < best_cost else best_ant
            best_cost = ant_total_cost if ant_total_cost < best_cost else best_cost 

        if online_phermone == False:
            offline_update(best_ant, Q, phermones)

        evaporate_phermone(phermone_decay, phermones)
        cost_per_iteration.append(tuple([i, best_cost]))
    return cost_per_iteration






def select_next_city(ant, phermones, alpha, beta, state_transition):

    possible_cities = list(set(ant.travelled) ^ set(cities))

    if state_transition > random.uniform(0, 1):
        probability_based(possible_cities, phermones, ant, alpha, beta)
    else:
        phermone_based(possible_cities, phermones, ant)

def probability_based(possible_cities, phermones, ant, alpha, beta):
    probabilities = []
    for city in possible_cities:
        probabilities.append(math.pow(phermones[ant.city[0] - 1][city[0]-1], alpha) / math.pow(euclidian_distance(ant.city, city), beta ))
    
    chosencity = random.choices(possible_cities, weights=probabilities, k=1)[0]
    ant.travelled.append(chosencity)
    ant.city = chosencity

def phermone_based(possible_cities, phermones, ant):
    highest_phermone_value = 0
    highest_city = None
    for city in possible_cities:
        highest_city = city if phermones[ant.city[0] - 1][city[0]-1] > highest_phermone_value else highest_city
        highest_phermone_value = phermones[ant.city[0] - 1][city[0]-1] if phermones[ant.city[0] - 1][city[0]-1] > highest_phermone_value else highest_phermone_value

    ant.travelled.append(highest_city)
    ant.city = highest_city

def euclidian_distance(origin, destination):
    return math.sqrt(math.pow(origin[1] - destination[1], 2) + math.pow(origin[2] - destination[2], 2))

def evaporate_phermone(phermone_decay, phermones):
  for x in range(len(phermones)):
    for y in range(len(phermones[x])):
            phermones[x][y] *= (1-phermone_decay)

def online_delayed_update(ant,Q, phermones):
    tau = Q / totalcost(ant.travelled)
    for x in range(len(ant.travelled)-1):
        phermones[ant.travelled[x][0] - 1][ant.travelled[x+1][0]-1] +=  tau
        phermones[ant.travelled[x+1][0] - 1][ant.travelled[x][0]-1] +=  tau
        

def offline_update(ant, Q, phermones):
    tau = Q / totalcost(ant.travelled)
    for x in range(len(ant.travelled)-1):
        phermones[ant.travelled[x][0] - 1][ant.travelled[x+1][0]-1] +=  tau
        phermones[ant.travelled[x+1][0] - 1][ant.travelled[x][0]-1] +=  tau

def totalcost(travelled):
    cost = 0
    for i in range(len(travelled) - 1):
        cost += euclidian_distance(travelled[i], travelled[i+1])
    return cost

def choose_part(part_chosen):
    alpha, beta, base_ph, ant_pop, phermone_decay, state_transition, online_phermone, Q, iter = 1,1,1,10,0.4,0.5,True, 5000,200
    if part_chosen == '0':
        values = ACO(alpha, beta, base_ph, ant_pop, phermone_decay, state_transition, online_phermone, Q, iter)

        plt.plot(*zip(*values))
        plt.xlabel('Iterations')
        plt.ylabel('TSP Tour Distance')
        plt.title('Shortest Distance Found Per Iteration(ONLINE)')
        plt.show()


    elif part_chosen == 'a':
        phermone_decays = [0.1, 0.4, 0.7]

        for phermone_decay in phermone_decays:
            values = ACO(alpha, beta, base_ph, ant_pop, phermone_decay, state_transition, online_phermone, Q, iter)
            plt.plot(*zip(*values), label= str(phermone_decay) + " Phermone Persistance")

        plt.xlabel('Iterations')
        plt.ylabel('TSP Tour Distance')
        plt.title('Shortest Distance Found Per Iteration')
        plt.legend()
        plt.show()


    elif part_chosen =='b':
        state_controls = [0.2, 0.5, 0.8]

        for state_transition in state_controls:
            values = ACO(alpha, beta, base_ph, ant_pop, phermone_decay, state_transition, online_phermone, Q, iter)
            plt.plot(*zip(*values), label= str(state_transition) + " State transition control parameter")

        plt.xlabel('Iterations')
        plt.ylabel('TSP Tour Distance')
        plt.title('Shortest Distance Found Per Iteration')
        plt.legend()
        plt.show()


    elif part_chosen =='c':
        pop_sizes = [5,10,15]

        for ant_pop in pop_sizes:
            values = ACO(alpha, beta, base_ph, ant_pop, phermone_decay, state_transition, online_phermone, Q, iter)
            plt.plot(*zip(*values), label= str(ant_pop) + " ANT POPULATION")

        plt.xlabel('Iterations')
        plt.ylabel('TSP Tour Distance')
        plt.title('Shortest Distance Found Per Iteration')
        plt.legend()
        plt.show()


    elif part_chosen == 'd':
        online_phermones = [True, False]
        for online_phermone in online_phermones:
            values = ACO(alpha, beta, base_ph, ant_pop, phermone_decay, state_transition, online_phermone, Q, iter)
            plt.plot(*zip(*values), label ="ONLINE UPDATE ON? " + str(online_phermone))
        plt.xlabel('Iterations')
        plt.ylabel('TSP Tour Distance')
        plt.title('Shortest Distance Found Per Iteration')
        plt.legend()
        plt.show()

    
choose_part(input("WHAT PART DO YOU WANT TO CHOOSE: "))