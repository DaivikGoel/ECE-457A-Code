import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random
import math

# global constants
iteration_number = 0
anneal_rate = 1
stopping_temperature = 1
movement_distance = 0.1
max_iterations_at_temp = 10
mini = 0
res = []

'''
simulated annealing takes an initial start point as input and performs simulated annealing 
for the easom function

returns time and corresponding easom function values for plotting as well as the solution
'''
def simulatedAnnealing(initial_point, initial_temperature, annealing_rate):
    global iteration_number, mini, res
    
    x_coord = []
    y_coord = []
    curr_solution = initial_point
    curr_time = 0
    curr_iter_at_temp = max_iterations_at_temp
    curr_temperature = initial_temperature
    curr_cost = easomFunction(curr_solution)
    while curr_temperature > stopping_temperature:
        if curr_cost < mini:
            res = curr_solution
            mini = curr_cost
        x_coord.append(curr_time)
        y_coord.append(curr_cost)
        next_solution = generateNeighboringSolution(curr_solution)
        next_cost = easomFunction(next_solution)
        print("current cost: " + str(curr_cost) + " current solution: " + str(curr_solution))
        if next_cost - curr_cost < 0: 
            # always accept improving move 
            curr_solution = next_solution
            curr_cost = next_cost
            curr_iter_at_temp = max_iterations_at_temp
        else: 
            acceptance_probability = math.exp((curr_cost-next_cost)/curr_temperature)
            if random.random() < acceptance_probability:
                # accept worse solution in this case otherwise reject the new solution
                curr_solution = next_solution
                curr_cost = next_cost
                curr_iter_at_temp = max_iterations_at_temp
            else: 
                curr_iter_at_temp -= 1
                if curr_iter_at_temp == 0:
                    return x_coord, y_coord, curr_solution
        curr_temperature = linearAnnealingSchedule(curr_temperature, annealing_rate)
        curr_time += 1
        iteration_number += 1
    x_coord.append(curr_time)
    y_coord.append(curr_cost)
    return x_coord, y_coord, curr_solution

'''
main function which calls simulated annealing function and plots results 
'''
def execute():
    intial_point = [0,0]
    initial_temperature = 1500
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'aquamarine', 'mediumseagreen', 'xkcd:sky blue']

    fontP = FontProperties()
    fontP.set_size('xx-small')
    fig = plt.figure()
    axes = fig.add_subplot(111)
    # experiment 1: selecting 10 different initial poitns randomly
    # for i in range(10):
    #     rand_point = generateRandomPoint()
    #     legend_point = list(map(round,rand_point))
    #     x_coord, y_coord, solution = simulatedAnnealing(rand_point, initial_temperature, 0)
    #     axes.scatter(x_coord, y_coord, s=10, c=colors[i], label=str(legend_point))
    
    # experiment 2: selecting 10 different initial temperatures in a reasonable range
    for i in range(10):
        rand_temp = generateRandomTemperature()
        x_coord, y_coord, solution = simulatedAnnealing(intial_point, rand_temp, 0)
        axes.scatter(x_coord, y_coord, s=10, c=colors[i], label=rand_temp)

    # experiment 3: selecting 10 different annealing schedules 
    # for i in range(10):
    #     linear_offset = random.randint(0, 50)
    #     x_coord, y_coord, solution = simulatedAnnealing(intial_point, initial_temperature, linear_offset)
    #     axes.scatter(x_coord, y_coord, s=10, c=colors[i], label="1 + " + str(linear_offset))
    print(res)
    plt.xlabel('time')
    plt.ylabel('solution profile')
    plt.legend(bbox_to_anchor=(0.993, 1), loc='upper left', prop=fontP)
    plt.show()


'''
cost function for this problem, we want to minimize the value of given easom function 
'''
def easomFunction(coordinate):
    x1 = coordinate[0]
    x2 = coordinate[1]
    return float(-math.cos(x1) * math.cos(x2) * math.exp(-pow(x1-math.pi, 2) - pow(x2-math.pi, 2)))


def geometricAnnealingSchedule(curr_temp):
    return curr_temp / (iteration_number + 1)


def linearAnnealingSchedule(curr_temp, input=0):
    return (curr_temp - anneal_rate - input)


def slowAnnealingSchedule(curr_temp):
    return curr_temp / (1 + curr_temp)

'''
selects a new solution from the neighborhood N(s) of the current solution, this is done 
by moving the x or y coordinate by a set constant
'''
def generateNeighboringSolution(curr_solution):
    # we choose between x or y 
    rand_axis = random.randint(0,1)
    rand_sign = [-1, 1][random.randrange(2)]
    curr_solution[rand_axis] += rand_sign * movement_distance
    return curr_solution


def generateRandomPoint():
    x1 = random.randint(-100, 100)
    x2 = random.randint(-100, 100)
    return [x1, x2]


'''
generates random temperature in an acceptable range, after testing the range 100-200 
seems to be reasonable to get a good result after execution
'''
def generateRandomTemperature(): 
    return random.randint(1000,2000)

# END OF FUNCTIONS - BEGINNING OF CODE
execute()

