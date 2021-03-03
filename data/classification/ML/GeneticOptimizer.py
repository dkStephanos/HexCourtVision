import csv
import random
import math
import pandas
import matplotlib.pyplot as plt
from copy import deepcopy

class GeneticOptimizer:
    def __init__(self,params_to_optimize,num_generations,population_size,mutation_rate,display_rate,rand_selection):
        self.params_to_optimize = params_to_optimize
        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.display_rate = display_rate
        self.rand_selection = rand_selection
        self.generations = []

    def set_model(self, clf_model):
        self.clf_model = clf_model

    # Modified to take a crossover strategy and gensave the image instead of display it, and return the data dict
    def plot_ga(self):
        generation_values = []
        best = []
        median = []
        worst = []
        gen = 1
        for g in self.generations:
            best_route = g[0]
            median_route = g[math.floor(self.population_size/2)]
            worst_route = g[self.population_size-1]
            best.append(best_route[1])
            median.append(median_route[1])
            worst.append(worst_route[1])
            generation_values.append(gen)
            gen = gen+1
        temp_data = {'Best': best, 'Median': median, 'Worst': worst }
        df = pandas.DataFrame(temp_data)
        plot = df.plot(title=f"Fitness Across Generations", xlabel="Generatons", ylabel="Fitness")
        plot.figure.savefig(f"FitnessAcrossGeneration.png")
        plt.clf()

        return temp_data

    def get_random_bool_param(self, param):
        return bool(random.getrandbits(1))

    def get_random_enum_param(self, param):
        index = random.randrange(0,len(param['range']),1)
        return param['range'][index]

    def get_random_int_param(self, param):
        return random.randrange(param['range'][0],param['range'][1],1)

    def get_random_float_param(self, param):
        return round(random.uniform(param['range'][0],param['range'][1]),3)

    def random_sample(self):
        get_field = {
            'bool': self.get_random_bool_param,
            'enum': self.get_random_enum_param,
            'int': self.get_random_int_param,
            'float': self.get_random_float_param,
        }

        chromosome = {}

        for key, param in self.params_to_optimize.items():
            chromosome[key] = get_field[param['type']](param)

        return chromosome

    # Returns a list containing chromosome,fitness ready to be inserted into a population
    def calculate_fitness(self, chromosome):
        """
        Fitness is the total route cost using the haversine distance.
        The GA should attempt to minimize the fitness; minimal fitness => best fitness
        """
        X_train, X_test, y_train, y_test = self.clf_model.split_test_data(chromosome['test_size'], chromosome['is_fixed'])
        self.clf_model.fit_and_predict(X_train, X_test, y_train)
        fitness = self.clf_model.get_f1_score(y_test)

        return [chromosome,fitness]


    ## initialize population
    def initialize_population(self):
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
    def repopulate(self, gen, random_selection):
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
            child = self.crossover(parent1, parent2)
            # Generate a random number, if it falls beneath the mutation_rate, perform a point swap mutation on the child
            if (random.random() < self.mutation_rate):
                child = self.mutate(child[0])
                
            new_population.append(child)

        # Sort the population by fitness
        new_population.sort(key=lambda x: x[1],reverse=True)

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

    def crossover(self, parent1, parent2):
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
        child = {}
        # Step through each item in the chromosome and randomly choose which
        #  parent's genetic material to select
        for key in parent1.keys():
            value = None
            if random.randint(0,1) == 0:
                value = parent1[key]
            else:
                value = parent2[key]
            child[key] = value

        return self.calculate_fitness(child)


    def mutate(self, chromosome):
        """
        Choose a param and reset it with a randomized value
        """
        get_field = {
            'bool': self.get_random_bool_param,
            'enum': self.get_random_enum_param,
            'int': self.get_random_int_param,
            'float': self.get_random_float_param,
        }

        # Copy the child
        mutant_child = deepcopy(chromosome)

        param_to_mutate = random.choice(list(self.params_to_optimize.keys()))
        mutant_child[param_to_mutate] = get_field[self.params_to_optimize[param_to_mutate]['type']](self.params_to_optimize[param_to_mutate])
        
        return self.calculate_fitness(mutant_child)

    # Modified to rake a crossover strategy and random_selection flag (defaulted to False)
    def run_ga(self):
        """
        Initialize and repopulate until you have reached the maximum generations
        """
        self.initialize_population()

        for gen in range(self.num_generations-1):      #Note, you already ran generation 1
            self.repopulate(gen+1, self.rand_selection)
            print(f"Starting generation {gen+1}")
            if (gen + 1) % self.display_rate == 0:
                print("Best Settings for Gen:") # Print the generation, and the best (lowest) fitness score in the population for that generation
                print(self.generations[gen][0])
                print("Fitness Score")
                print(f"{round(self.generations[gen][0][1],3)*100}%")
