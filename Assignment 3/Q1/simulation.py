from algo import GeneticAlgorithm
from chromosome import Chromosome
import random
import PID

class Simulation:

    def __init__(self, config):
        self.config = config
        self.algo = GeneticAlgorithm(self.config)
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
            # if (chromosomeIndex % 10 == 0):
            #     print(chromosomeIndex)
                
            curr_chromosome = self.population[chromosomeIndex]
            self.fitness_values.append(self.algo.fitness_of_chromosome(curr_chromosome))


        # generate a new population based on fitness values
        for chromosomeIndex in range(self.population_size):
            
            # Fitness Proportionate Selection:
            selected_parents = []

            while len(selected_parents) < 2:
                if len(selected_parents) == 1:  
                    parent_1 = selected_parents[0]
                    parent_2 = self.algo.selection(self.fitness_values, self.population) 
                    # in case we get the exact same parent back:
                    if (parent_1 == parent_2):
                        continue

                result = self.algo.selection(self.fitness_values, self.population)
                if result:
                    selected_parents.append(result)


            # crossover
            offspring = self.algo.crossover(selected_parents[0], selected_parents[1])

            # mutation  
            offspring = self.algo.mutation(offspring)

            #calculate and set fitness score:
            self.algo.fitness_of_chromosome(offspring)

            new_population.append(offspring)
        
        self.population = new_population

        return self.population

