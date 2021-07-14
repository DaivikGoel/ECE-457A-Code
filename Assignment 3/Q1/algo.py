import random
import math
import numpy as np

from chromosome import Chromosome
import PID

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.population_size = self.config['population_size']
        self.crossover_rate = self.config['crossover_rate']
        self.mutation_prob = self.config['mutation_probability']


    def chromosome_valid(self, c):
        return c.kp >= self.config['kp_low'] and c.kp <= self.config['kp_high'] and c.td >= self.config['td_low'] and c.td <= self.config['td_high'] and c.ti >= self.config['ti_low'] and c.ti <= self.config['ti_high']


    # returns the fitness evaluted by 1/ise, where ise is calculated from the transfer function
    def fitness_of_chromosome(self, chromosome):
        
        ise = PID.evaluate_transfer_fn(chromosome.kp, chromosome.ti, chromosome.td)
        f_score = 1/ise

        # add f_score to the chromosome obj as they are calculated
        chromosome.fitness = f_score
        return f_score
    

    # picks parents whose chance of being selected is proportional to its fitness, higher fitness individuals are more likley to be selected
    def selection(self, fitness_vals, population):

        normalized_fitness_vals = self.normalize_list(fitness_vals)
        parent_prob = random.uniform(0, 1)

        curr_sum = 0
        # use rolling sum to select individuals:
        for i in range(self.population_size):
            next_sum = curr_sum + fitness_vals[i]
            
            # if number > probability but less than next probability, select: 
            if parent_prob <= next_sum and parent_prob >= curr_sum:
                return population[i]

            curr_sum = next_sum
 
        return None
        

    def crossover(self, c1, c2):
        # no crossover applied, one of the parent is returned:
        if random.uniform(0, 1) > self.crossover_rate:
            if random.uniform(0, 1) < 0.5:
                return c1
            else: 
                return c2

        rand = random.uniform(0, 1)
        if rand < 1.0/6:
            return Chromosome(c1.kp,c1.td, c2.ti)
        elif rand < 2.0/6:
            return Chromosome(c1.kp, c2.td, c1.ti)
        elif rand < 3.0/6:
            return Chromosome(c1.kp, c2.td, c2.ti)
        elif rand < 4.0/6:
            return Chromosome(c2.kp, c1.td, c1.ti)
        elif rand < 5.0/6:
            return Chromosome(c2.kp,c1.td, c2.ti)
        else:
            return Chromosome(c2.kp,c2.td, c1.ti)


    def mutation(self, chromosome):
        # the mutation values have been adjusted according to the range of allowed KP, TD, and TI values
        if random.uniform(0, 1) > self.mutation_prob:
            return chromosome

        chromosome = self.mutate(chromosome)

        # only return if curr mutated chromosome is valid
        while not self.chromosome_valid(chromosome):
            chromosome = self.mutate(chromosome)

        return chromosome


    def mutate(self, chromosome):
        rand_num = random.uniform(0, 1) 
        if rand_num < self.mutation_prob / 3:
            chromosome.kp = round(chromosome.kp + random.uniform(-0.05, 0.05), 2)
        if chromosome.kp < 0:
            chromosome.kp = round(random.uniform(2, 8) + random.uniform(-0.05, 0.05), 2)

        elif rand_num < self.mutation_prob * 2/3:
            chromosome.td = round(chromosome.td + random.uniform(-0.07, 0.07), 2)
        if chromosome.td < 0:
            chromosome.td = round(random.uniform(1.05, 9.42) + random.uniform(-0.07, 0.07), 2)

        elif rand_num < self.mutation_prob:
            chromosome.ti = round(chromosome.ti + random.uniform(-0.018, 0.018), 2)
        if chromosome.ti < 0:
            chromosome.ti = round(random.uniform(0.26, 2.37) + random.uniform(-0.018, 0.018), 2)

        return chromosome


    # to normalize against the sum, list values will take on values in (0, 1)
    def normalize_list(self, vals_list):
        return [x / sum(vals_list) for x in vals_list]

