from algo import GeneticAlgorithm
from chromosome import Chromosome
import random
import PID

class Simulation:

    def __init__(self, config):
        self.config = config
        self.algorithm = GeneticAlgorithm(self.config)
        self.population_size = self.config['population_size']
        self.generate_initial_population()


    def generate_initial_population(self):
        """
        Generate random population of n chromosomes, and create a random genome
        """
        self.population = []
        for chromosome in range(self.population_size):
            # create a random chromosome with a random param values:

            kp = round(random.uniform(2, 8), 2)
            td = round(random.uniform(1.05, 9.42), 2)
            ti = round(random.uniform(0.26, 2.37), 2)
            
            self.population.append(Chromosome(kp,td,ti))
            

    def generate_new_population(self):
        new_population = []
        self.fitness_values = []

        # get fitness scores of curr population
        for chromosomeIndex in range(self.population_size):
            if (chromosomeIndex % 10 == 0):
                print(chromosomeIndex)
                
            self.fitness_values.append(self.fitness_of_chromosome(chromosomeIndex))

        # TODO: generate a new population based on fitness values
            


    # returns the fitness evaluted by 1/ise, where ise is calculated from the transfer function
    def fitness_of_chromosome(self, index):
        # returns fitness function value for curr chromosome

        curr_chromosome = self.population[index]
        ise = PID.evaluate_transfer_fn(curr_chromosome.kp, curr_chromosome.ti, curr_chromosome.td)
        f_score = 1/ise

        curr_chromosome.fitness = f_score
        return f_score
