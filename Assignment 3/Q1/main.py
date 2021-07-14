import math
import statistics
from simulation import Simulation
from config import config
import matplotlib.pyplot as plt
import numpy as np
import PID

print('running Question 1')

# kp_values = []
# td_values = []
# ti_values = []

simulation = Simulation(config)
simulation.generate_initial_population()

max_fitness_list = []
avg_fitness_list = []
median_fitness_list = []

for i in range(config['num_generations']):
    simulation.generate_new_population()
    population = simulation.population

    fitness_values = []
    for p in simulation.population:
        fitness_values.append(p._fitness)
        # kp_values.append(p.kp)
        # td_values.append(p.td)
        # ti_values.append(p.ti)
        # print('kp: ', p.kp, ' td: ', p.td, ' ti: ', p.ti, ' fitness: ', p._fitness)

    max_fit = max(fitness_values)
    max_fitness_list.append(max_fit)
    
    avg_fit = np.mean(fitness_values)
    avg_fitness_list.append(avg_fit)

    median_fit = statistics.median(fitness_values)
    median_fitness_list.append(median_fit)


    print('max fitness of iteration ', i, ': ', "{:.5f}".format(max_fit))
    print('avg fitness of iteration ', i, ': ', "{:.5f}".format(avg_fit))
    print('median fitness of iteration ', i, ': ', "{:.5f}".format(median_fit))
    print('')


best_soln_line = np.array(max_fitness_list)
avg_soln_line = np.array(avg_fitness_list)
median_soln_line = np.array(median_fitness_list)


plt.plot(best_soln_line, label="best fitness")
plt.plot(avg_soln_line, label="avg fitness")
plt.plot(median_soln_line, label="median fitness")
plt.legend(loc="upper left")

plt.title("fitness vs generations")
plt.xlabel("generations")
plt.ylabel("fitness score")

plt.show()
