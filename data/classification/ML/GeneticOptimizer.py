import csv
import random
import math
import pandas
import matplotlib.pyplot as plt
from copy import deepcopy

class GeneticOptimizer:
    def __init__(self,initial_configuration={}, params_to_optimize={},num_generations=100,population_size=200,mutation_rate=0.1,display_rate=20,init_crossover_strategy='multipoint',rand_selection=False):
        self.initial_configuration = initial_configuration
        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.display_rate = display_rate
        self.init_crossover_strategy = init_crossover_strategy
        self.rand_selection = rand_selection
        self.generations = []

    def set_model(self, clf_model):
        self.clf_model = clf_model

    # Modified to take a crossover strategy and gensave the image instead of display it, and return the data dict
    def plot_ga(self, crossover_strategy):
        generation_values = []
        best = []
        worst = []
        gen = 1
        for g in self.generations:
            best_route = g[0]
            worst_route = g[self.population_size-1]
            best.append(best_route[1])
            worst.append(worst_route[1])
            generation_values.append(gen)
            gen = gen+1
        temp_data = {'Best':best,'Worst':worst }
        df = pandas.DataFrame(temp_data)
        plot = df.plot(title=f"Fitness Across Generations: {crossover_strategy} crossover", xlabel="Generatons", ylabel="Fitness")
        plot.figure.savefig(f"FitnessAcrossGenerations_{crossover_strategy}-crossover.png")
        plt.clf()

        return temp_data

    def random_sample(self):
        pass

    # Returns a list containing chromosome,fitness ready to be inserted into a population
    def calculate_fitness(self, chromosome):
        """
        Fitness is the total route cost using the haversine distance.
        The GA should attempt to minimize the fitness; minimal fitness => best fitness
        """
        fitness = self.clf_model.train_and_predict()

        return [chromosome,fitness]


    ## initialize population
    def initialize_population(self, ):
        """
        Initialize the population by creating self.population_size chromosomes.
        Each chromosome represents the index of the point in the points list.
        Sorts the population by fitness and adds it to the generations list.
        """
        my_population = []

        # Loop through creating chromosomes until we fill the population
        for chromosome in range(0, self.population_size):
            # Shuffle the list of points and calculate the fitness of the path which returns the [chromosme,fitness] ready to be added to the population
            my_population.append(self.calculate_fitness(self.random_sample()))     

        # Sort the population by fitness
        my_population.sort(key=lambda x: x[1])

        self.generations.append(my_population)

    # Takes the index to the generation to repopulate from, and a crossover strategy (accepts: uniform, singlepoint, multipoint)
    def repopulate(self, gen, crossover_strategy, random_selection=False):
        """
        Creates a new generation by repopulation based on the previous generation.
        Calls selection, crossover, and mutate to create a child chromosome. Calculates fitness
        and continues until the population is full. Sorts the population by fitness
        and adds it to the generations list.
        """
        ## Ensure you keep the best of the best from the previous generation
        retain = math.ceil(self.population_size*0.025)
        new_population = self.generations[gen-1][:retain]

        ## Conduct selection, reproduction, and mutation operations to fill the rest of the population
        while len(new_population) < self.population_size:
            # Select the two parents from the growing population
            parent1, parent2 = self.selection(gen, random_selection)
            # Generate the child according to the designated crossover_strategy
            child = self.crossover(parent1, parent2, crossover_strategy)
            # Generate a random number, if it falls beneath the mutation_rate, perform a point swap mutation on the child
            if (random.random() < self.mutation_rate):
                child = self.mutate(child[0])
                
            new_population.append(child)

        # Sort the population by fitness
        new_population.sort(key=lambda x: x[1])

        self.generations.append(new_population)

    # Adopted and modified from Genetic Search Algorithm lab
    # Set rand to True to divert typical functionality and choose parents completely at random
    def selection(self, gen, rand=False):
        '''
        Selects parents from the given population, assuming that the population is
        sorted from best to worst fitness.

        Parameters
        ----------
        population : list of lists
            Each item in the population is in the form [chromosome,fitness]

        Returns
        -------
        parent1 : list of int
            The chromosome chosen as parent1
        parent2 : list of int
            The chromosome chosen as parent2

        '''
        # Set the elitism factor and calculate the max index
        if rand == False:
            factor = 0.5	# Select from top 50%
            high = math.ceil(self.population_size*factor)
        else:
            high = self.population_size - 1

        # Choose parents randomly
        parent1 = self.generations[gen-1][random.randint(0,high)][0]
        parent2 = self.generations[gen-1][random.randint(0,high)][0]

        # If the same parent is chosen, pick another
        # we can get stuck here if we converge early, if we pick the same parent ten times in a row, just bail out
        count = 0
        while str(parent1) == str(parent2):
            parent2 = self.generations[gen-1][random.randint(0,high)][0]
            count += 1
            if count == 10:
                break

        return parent1, parent2

    # Adopted and modified from Genetic Search Algorithm lab
    # Set crossover_strategy to "singlepoint"/"multipoint" to divert from typical behavior and instead perform a singlepoint/multipoint reproduction strategy
    def crossover(self, parent1, parent2, crossover_strategy="uniform"):
        '''
        Parameters
        ----------
        parent1 : list of int
            A chromosome that lists the steps to take
        parent2 : list of int
            A chromosome that lists the steps to take

        Returns
        -------
        list in the form [chromosome,fitness]
            The child chromosome and its fitness value

        '''
        # Initialization
        child = []
        chromosome_size = len(parent1)
        if crossover_strategy == "singlepoint":
            # Randomly choose a split point
            split_point = chromosome_size - random.randint(0, chromosome_size)
            child = parent1[:split_point] + parent2[split_point:]
        elif crossover_strategy == "multipoint":
            points = []
            while len(points) < 2: 
                split_point = chromosome_size - random.randint(0, chromosome_size) 
                if split_point not in points:
                    points.append(split_point)
            points.sort()
            child = parent1[:points[0]] + parent2[points[0]:points[1]] + parent1[points[1]:]
        else:
            # Step through each item in the chromosome and randomly choose which
            #  parent's genetic material to select
            for i in range(0, chromosome_size):
                bit = None
                if random.randint(0,1) == 0:
                    bit = parent1[i]
                else:
                    bit = parent2[i]
                child.append(bit)

        return self.calculate_fitness(child)


    def mutate(self, chromosome):
        """
        Strategy: swap two pairs of points. Return the chromosome after mutation.
        """
        # Copy the child
        mutant_child = deepcopy(chromosome)
        # Select two random points
        point1, point2 = random.sample(range(len(mutant_child)), 2)
        #Swap the points
        mutant_child[point1], mutant_child[point2] = mutant_child[point2], mutant_child[point1]
        
        return self.calculate_fitness(mutant_child)

    # Modified to rake a crossover strategy and random_selection flag (defaulted to False)
    def run_ga(self, crossover_strategy, random_selection=False):
        """
        Initialize and repopulate until you have reached the maximum generations
        """
        self.initialize_population()

        for gen in range(self.num_generations-1):      #Note, you already ran generation 1
            self.repopulate(gen+1, crossover_strategy, random_selection)
            if gen % self.display_rate == 0:
                print("Best Geneartion:") # Print the generation, and the best (lowest) fitness score in the population for that generation
                print(self.generations[gen])
                print("Fitness Score")
                print(self.generations[gen][0][1])