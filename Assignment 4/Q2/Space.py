import random
import math
import numpy as np

W = 0.9
c1 = 2.1
c2 = 2.3
success_count = 0 
fail_count = 0

class Space():
    def __init__(self, _c1, _c2, _W, num_of_particles):
        global c1, c2, W, success_count, fail_count
        c1 = _c1
        c2 = _c2
        W = _W

        self.num_of_particles = num_of_particles
        self.particles = []

        # trying to minimize this:
        self.global_best_val = float('inf') 
        self.best_particle = None

        # randomly assign best_val_posn
        i = (-1) ** (bool(random.getrandbits(1))) * random.random()*5
        j = (-1) ** (bool(random.getrandbits(1))) * random.random()*5
        self.global_best_posn = np.array([i, j])


    def calculate_fitness(self, particle):
        # z = (4 - 2.1x^2 + (x^4)/3) x^2 + x*y + (-4 + 4y^2) * y^2
        x, y = particle.position[0], particle.position[1]
        return (4 - 2.1 * x**2 + (x**4)/3) * x**2 + x*y + (-4 + 4 * y**2) * y**2


    def set_individual_best(self):
        ind_fitness_scores = []
        for p in self.particles:
            fitness_score = self.calculate_fitness(p)
            ind_fitness_scores.append(fitness_score)
            # finding lowest score here
            if p.best_value > fitness_score:
                p.best_value = fitness_score
                best_val_so_far = fitness_score
                p.best_position = p.position
        return ind_fitness_scores


    def set_global_best(self):
        global fail_count, success_count

        best_val_so_far = float('inf') 
        for p in self.particles:
            fitness_score = self.calculate_fitness(p)

            if (self.best_particle == p):
                fail_count +=1
                success_count = 0

            # new best particle found:
            if(self.global_best_val > fitness_score):
                if (self.best_particle == p):
                    success_count+=1
                    fail_count = 0
                else:
                    # success and fail both set to 0 if best particle changes
                    success_count = 0
                    fail_count = 0
                self.best_particle = p # update best particle

                self.global_best_val = fitness_score
                self.global_best_posn = p.position
        

    def move_particles_inertial(self):
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


    def move_particles_constricton_factor(self):
        phi  = c1 + c2
        if (phi <= 4):
            raise ValueError('c1 + c2 should be greater than 4')
        K = 2 / math.fabs((2 - phi - math.sqrt(phi**2 - 4*phi)))

        for particle in self.particles:
            individual_component = c1 * random.random() * (particle.best_position - particle.position)
            social_component = c2 * random.random() * (self.global_best_posn - particle.position)

            # vi(t+1) = K · (vi(t) + c1 · rand1·(pi - xi(t)) + c2 · rand2 · (p best - xi(t)))
            particle.velocity = K * (particle.velocity + individual_component + social_component)
            particle.update_posn()


    def move_particles_guranteed_converge(self, S_c, F_c):
        P = 1 
        for particle in self.particles:
            if success_count > S_c: 
                P = 2*P
            elif fail_count > F_c:
                P = 0.5*P

            particle.velocity = W * particle.velocity - particle.position + particle.best_position + P * random.uniform(-1, 1)
            particle.update_posn()

        pass
