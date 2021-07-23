from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
import numpy as np
import operator
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

toolbox = base.Toolbox()

def if_then_else(condition, out1, out2):
    return out1 if condition else out2


'''
prepares deap toolbox and individual for multiplexer problems
'''
def multiplexer(num_select_bits):
    num_data_bits = pow(2,num_select_bits)
    total_bits = num_select_bits + num_data_bits

    inputs = []
    generateBinaryPermutations(total_bits, [], inputs, 0)
    outputs = [None] * pow(2, total_bits)
    # Calculating mux output for all permutations of inputs
    for i in range(pow(2, total_bits)):
        indexOutput = num_select_bits
        for j, val in enumerate(inputs[i][:num_select_bits]):
            if val:
                indexOutput += pow(2, j)
        outputs[i] = inputs[i][indexOutput]

    def evalMultiplexer(individual):
        func = toolbox.compile(expr=individual)
        return sum(func(*in_) == out for in_, out in zip(inputs, outputs)),

    pset = gp.PrimitiveSet("MAIN", total_bits, "IN")
    pset.addPrimitive(operator.and_, 2)
    pset.addPrimitive(operator.or_, 2)
    pset.addPrimitive(operator.not_, 1)
    pset.addPrimitive(if_then_else, 3)
    pset.addTerminal(1)
    pset.addTerminal(0)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

    toolbox.register("expr", gp.genFull, pset=pset, min_=2, max_=4)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)
    toolbox.register("evaluate", evalMultiplexer)
    toolbox.register("select", tools.selTournament, tournsize=8)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


'''
prepares deap toolbox and individual for 16-middle-3 problems
'''
def middle():
    inputs = []
    generateBinaryPermutations(16, [], inputs, 0)
    outputs = [None] * pow(2, 16)
    # Calculating mux output for all permutations of inputs
    for i in range(pow(2, 16)):
        total = 0
        for j, val in enumerate(inputs[i]):
            if val:
                total += 1
        if total >= 7 and total <= 9:
            outputs[i] = 1
        else: 
            outputs[i] = 0

    def evalMultiplexer(individual):
        func = toolbox.compile(expr=individual)
        return sum(func(*in_) == out for in_, out in zip(inputs, outputs)),

    pset = gp.PrimitiveSet("MAIN", 16, "IN")
    pset.addPrimitive(operator.and_, 2)
    pset.addPrimitive(operator.or_, 2)
    pset.addPrimitive(operator.not_, 1)
    pset.addPrimitive(if_then_else, 3)
    pset.addTerminal(1)
    pset.addTerminal(0)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

    toolbox.register("expr", gp.genFull, pset=pset, min_=2, max_=4)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)
    toolbox.register("evaluate", evalMultiplexer)
    toolbox.register("select", tools.selTournament, tournsize=8)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


'''
generates all possible binary inputs for length n
'''
def generateBinaryPermutations(n, curr, inputs, i):
    if i == n:
        inputs.append(curr.copy())
        return
    curr.append(0)
    generateBinaryPermutations(n, curr, inputs, i+1)
    curr.pop() 

    curr.append(1)
    generateBinaryPermutations(n, curr, inputs, i+1)
    curr.pop()


'''
function for setting up deap for multiplexer problems and plotting solutions
'''
def plot_multiplexer(num_select_bits, total_gens):
    multiplexer(num_select_bits)
    random.seed()
    pop = toolbox.population(n=500)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", np.mean)
    stats.register("Max", max)
    
    generations = algorithms.eaSimple(pop, toolbox, 0.8, 0.1, total_gens, stats, halloffame=hof)
    best_generational_fitness = []
    for i, gen in enumerate(generations[1]):
        best_generational_fitness.append(gen['Max'][0])
    print(hof[0])

    plt.plot(best_generational_fitness)
    plt.ylabel('Best Iteration Fitness')
    plt.xlabel('Generation number')
    plt.show()

def plot_middle(total_gens):
    middle()
    random.seed()
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", np.mean)
    stats.register("Max", max)
    
    generations = algorithms.eaSimple(pop, toolbox, 0.8, 0.1, total_gens, stats, halloffame=hof)
    best_generational_fitness = []
    for i, gen in enumerate(generations[1]):
        best_generational_fitness.append(gen['Max'][0])
    print(hof[0])

    plt.plot(best_generational_fitness)
    plt.ylabel('Best Iteration Fitness')
    plt.xlabel('Generation number')
    plt.show()


# Execute code below 
# plot_multiplexer(3, 70)
plot_middle(40)