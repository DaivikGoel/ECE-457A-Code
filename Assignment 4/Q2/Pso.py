import random
import numpy as np 
from Space import Space
from Particle import Particle

z_target = -1.031628
target_err = 0.0001
num_of_iterations = 250

search_space = Space(z_target, target_err, num_of_iterations)

particles_arr = [Particle() for _ in range(search_space.num_of_particles)]
# for i in range(search_space.num_of_particles):
#     particles_arr[i] = Particle()

# search_space.particles = particles_arr

search_space.particles = particles_arr


iteration = 0
while(iteration < num_of_iterations):
    search_space.set_individual_best()
    search_space.set_global_best()
    search_space.move_particles()

    iteration += 1

print('with ', num_of_iterations, ' iteraions')
print('best global x and y values: ', search_space.global_best_posn)
print('best global z: ', search_space.global_best_val)
