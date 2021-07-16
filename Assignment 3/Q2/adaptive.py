import numpy as np
import math
import array
from random import uniform
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from deap import base
from deap import creator
from deap import benchmarks
from deap import tools
from deap import cma
from deap import algorithms


# global constants 
MAX_ITERATIONS = 500
G = 10
n = 10

'''
main function which calls one plus one ES with multiple c values and plots results
'''
def run_trials():
    num_trials = 50
    std_dev = 0.1/(2*math.sqrt(3))
    starting_individual = [uniform(-5.12, 5.12) for i in range(n)]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'aquamarine', 'mediumseagreen', 'xkcd:sky blue']
    c_arr = [0.6, 0.8, 1]
    fontP = FontProperties()
    fontP.set_size('xx-small')
    fig = plt.figure()
    axes = fig.add_subplot(111)

    for j in range(len(c_arr)):
        c = c_arr[j]
        arr = [0 for i in range(MAX_ITERATIONS)]
        for i in range(num_trials):
            curr_vals = one_plus_one(std_dev*std_dev, starting_individual, n, c)
            arr = np.add(arr, curr_vals)
        for i in range(MAX_ITERATIONS):
            arr[i] = arr[i]/num_trials
        axes.scatter([i for i in range(MAX_ITERATIONS)], arr, s=10, c=colors[j], label="c=" + str(c))

    
    # plotting trial results
    plt.plot(arr)
    plt.ylabel('Average cost')
    plt.xlabel('Generation number')
    plt.legend(bbox_to_anchor=(0.993, 1), loc='upper left', prop=fontP)
    plt.show()


'''
main function which calls one plus one ES using deap and without deap and plots results
'''
def run_trials_deap(c):
    num_trials = 50
    std_dev = 0.1/(2*math.sqrt(3))
    starting_individual = [uniform(-5.12, 5.12) for i in range(n)]
    fontP = FontProperties()
    fontP.set_size('xx-small')
    fig = plt.figure()
    axes = fig.add_subplot(111)
  
    arr = [0 for i in range(MAX_ITERATIONS)]
    for i in range(num_trials):
        curr_vals = one_plus_one(std_dev*std_dev, starting_individual, n, c)
        arr = np.add(arr, curr_vals)
    for i in range(MAX_ITERATIONS):
        arr[i] = arr[i]/num_trials
    axes.scatter([i for i in range(MAX_ITERATIONS)], arr, s=10, c='b', label="Non-deap" + str(c))

    arr = [0 for i in range(MAX_ITERATIONS)]
    for i in range(num_trials):
        curr_vals = one_plus_one_deap(std_dev*std_dev, starting_individual, n, c)
        arr = np.add(arr, curr_vals)
    for i in range(MAX_ITERATIONS):
        arr[i] = arr[i]/num_trials
    axes.scatter([i for i in range(MAX_ITERATIONS)], arr, s=10, c='g', label="Deap" + str(c))

    
    # plotting trial results
    plt.plot(arr)
    plt.ylabel('Average cost')
    plt.xlabel('Generation number')
    plt.legend(bbox_to_anchor=(0.993, 1), loc='upper left', prop=fontP)
    plt.show()


'''
update function inputted into deap toolbox
'''
def update(ind, mu, std):
    r = [np.random.normal(0, math.pow(std,2)) for i in range(n)]
    next_individual = add_vectors(ind, r)
    ind = next_individual


'''
1+1 ES algorithm implementation using deap
'''
def one_plus_one_deap(variance, initial_individual, n, c):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()                  
    toolbox.register("update", update)
    toolbox.register("evaluate", benchmarks.sphere)

    # Using One Plus Lambda algorithm with lambda set to 1
    parent = creator.Individual(initial_individual)
    parent.fitness.values = toolbox.evaluate(parent)
    
    strategy = cma.StrategyOnePlusLambda(parent, sigma=c, lambda_=1)
    toolbox.register("generate", strategy.generate, ind_init=creator.Individual)
    toolbox.register("update", strategy.update)

    hof = tools.HallOfFame(1)    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
   
    generations = algorithms.eaGenerateUpdate(toolbox, ngen=MAX_ITERATIONS, halloffame=hof, stats=stats)
    res = []
    for i, gen in enumerate(generations[1]):
        print(gen)
        res.append(gen['avg'])
    return res


'''
1+1 ES algorithm implementation
'''
def one_plus_one(variance, initial_individual, n, c):
    res = []
    current_individual = initial_individual
    current_iterations = 0
    mutation_record = []
    while current_iterations < MAX_ITERATIONS: 
        res.append(ken_function(current_individual,n))
        r = [np.random.normal(0, variance) for i in range(n)]
        next_individual = add_vectors(current_individual, r)

        # determining if next individual is better than current - if so this is our new individual
        if ken_function(next_individual,n) < ken_function(current_individual,n):
            current_individual = next_individual
            mutation_record.append(1)
        else:
            mutation_record.append(0)
        
        # calculating new variance
        if len(mutation_record) > G and get_phi(mutation_record) < 0.2:
            variance = variance * c * c
        else:
            variance = variance/(c*c)
        current_iterations += 1
    return res


'''
adding two vectors taking into account maximum and minimum bounds
'''
def add_vectors(individual, r):
    res = []
    for i in range(len(individual)):
        sum = individual[i] + r[i]

        # keeping the function in bounds
        if sum > 0:
            sum = min(sum, 5.12)
        else: 
            sum = max(sum, -5.12)
        res.append(sum)
    return res


'''
ken function used as a cost function for this class
'''
def ken_function(arr, n):
    res = 0
    for i in range(n):
        res += arr[i]*arr[i]
    return res


'''
returns phi which is defined as proportion of successful mutations in last G generations
'''
def get_phi(mutation_record):
    total = 0
    mutation_record = mutation_record[-G:]
    for i in range(len(mutation_record)):
        total += mutation_record[i]
    return total/G


# Call functions here 
# run_trials_deap(0.8)
run_trials()