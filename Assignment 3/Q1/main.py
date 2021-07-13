import math
from simulation import Simulation
from config import config
import matplotlib.pyplot as plt
import numpy as np
import PID

print('running Question 1')

kp_values = []
td_values = []
ti_values = []

simulation = Simulation(config)
simulation.generate_initial_population()

for i in range(config['num_generations']):
    simulation.generate_new_population()
    population = simulation.population

    fitness_values = []
    for p in simulation.population:
        fitness_values.append(p._fitness)
        print('kp: ', p.kp, ' td: ', p.td, ' ti: ', p.ti, ' fitness: ', p._fitness)

    print('max fitness of iteration ', i, ': ', "{:.5f}".format(max(fitness_values)))
    print('avg fitness of iteration ', i, ': ', "{:.5f}".format(np.mean(fitness_values)))
