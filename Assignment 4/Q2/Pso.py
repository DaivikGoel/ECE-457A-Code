import random
import numpy as np 
from Space import Space
from Particle import Particle
import matplotlib.pyplot as plt

C1 = float(input("input C1 to use: "))
C2 = float(input("input C2 to use: "))
W = float(input("input W to use: "))
S_c = 3
F_c = 3

num_of_iterations = int(input("type the number of iterations to run: "))
num_of_particles = int(input("type the number of particles to simulate: "))

best_individual_fitness_list = []
avg_individual_fitness_list = []

search_space = Space(C1, C2, W, num_of_particles)
particles_arr = [Particle() for _ in range(search_space.num_of_particles)]
search_space.particles = particles_arr


iteration = 0
while(iteration < num_of_iterations):
    ind_fitness_scores = search_space.set_individual_best()
    best_individual_fitness_list.append(np.min(ind_fitness_scores))
    avg_individual_fitness_list.append(search_space.global_best_val)
    search_space.set_global_best()

    search_space.move_particles_inertial()
    # search_space.move_particles_constricton_factor()
    # search_space.move_particles_guranteed_converge(S_c, F_c)
    iteration += 1


print('with ', num_of_iterations, ' iterations')
print('best global x and y values: ', search_space.global_best_posn)
print('best global z: ', search_space.global_best_val)



best_soln_line = np.array(best_individual_fitness_list)
avg_soln_line = np.array(avg_individual_fitness_list)

plt.plot(best_soln_line, label="best fitness")
plt.plot(avg_soln_line, label="avg fitness")
plt.legend(loc="upper left")

plt.title("fitness vs iterations with partcles: "+ str(num_of_particles) + ", C1:" + str(round(C1, 2)) + ", C2:" + str(round(C2, 2)) + ", W:" + str(W))
plt.xlabel("iteration")
plt.ylabel("fitness score")

plt.show()

