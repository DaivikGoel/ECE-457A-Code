import random
import numpy as np

W = 0.9
c1 = 0.7
c2 = 0.7

class Space():
    def __init__(self, target, target_error, num_of_particles):
        self.target = target
        self.target_error = target_error
        self.num_of_particles = num_of_particles
        self.particles = []

        # trying to minimize this:
        self.global_best_val = float('inf') 

        # randomly assign best_val_posn
        i = (-1) ** (bool(random.getrandbits(1))) * random.random()*5
        j = (-1) ** (bool(random.getrandbits(1))) * random.random()*5
        self.global_best_posn = np.array([i, j])


    def calculate_fitness(self, particle):
        # z = (4 - 2.1x^2 + (x^4)/3) x^2 + x*y + (-4 + 4y^2) * y^2
        x, y = particle.position[0], particle.position[1]
        return (4 - 2.1 * x**2 + (x**4)/3) * x**2 + x*y + (-4 + 4 * y**2) * y**2


    def set_individual_best(self):
        for p in self.particles:
            fitness_score = self.calculate_fitness(p)
            # finding lowest score here
            if p.best_value > fitness_score:
                p.best_value = fitness_score
                p.best_position = p.position


    def set_global_best(self):
        for p in self.particles:
            fitness_score = self.calculate_fitness(p)
            if(self.global_best_val > fitness_score):
                self.global_best_val = fitness_score
                self.global_best_posn = p.position
        

    def move_particles(self):
        """ 
        next_velocity = (W * curr_velocity) + c1 * rand1 * (Particle's best_posn - Particle's curr_posn) + c2 * rand2 * (global best posn - particle's curr_posn)
        next position = curr_position + next_velocity 
        """

        for particle in self.particles:
            global W # change W if needed
            individual_component = c1 * random.random() * (particle.best_position - particle.position)
            social_component = c2 * random.random() * (self.global_best_posn - particle.position)
            
            # update velocity and posn of each particle:
            particle.velocity = W * particle.velocity + individual_component + social_component
            particle.update_posn()


