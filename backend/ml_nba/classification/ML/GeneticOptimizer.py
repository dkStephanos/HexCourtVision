import csv
import random
import math
import pandas
import matplotlib.pyplot as plt
from copy import deepcopy

class GeneticOptimizer:
    def __init__(self,params_to_optimize,num_generations,population_size,mutation_rate,display_rate,rand_selection,test_size=.2,is_fixed=True):
        self.params_to_optimize = params_to_optimize
        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.display_rate = display_rate
        self.rand_selection = rand_selection
        self.generations = []
        self.test_size = test_size
        self.is_fixed = is_fixed

    def set_model(self, clf_model):
        self.clf_model = clf_model

    # Modified to take a crossover strategy and gensave the image instead of display it, and return the data dict
    def plot_ga(self, dir):
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
        plot.figure.savefig(f"{dir}FitnessAcrossGeneration.png")
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

    def random_sample_features(self):
        return random.sample(self.clf_model.X.columns.values.tolist(), random.randint(3,len(self.clf_model.X.columns.values.tolist())))

    # Returns a list containing chromosome,fitness ready to be inserted into a population
    def calculate_fitness(self, chromosome):
        """
        Fitness is the total route cost using the haversine distance.
        The GA should attempt to minimize the fitness; minimal fitness => best fitness
        """
        X_train, X_test, y_train, y_test = self.clf_model.split_test_data(self.test_size, self.is_fixed)
        self.clf_model.fit_and_predict(X_train, X_test, y_train)
        fitness = self.clf_model.get_f1_score(y_test)

        return [chromosome,fitness]

    # Returns a list containing chromosome,fitness ready to be inserted into a population
    def calculate_fitness_features(self, chromosome):
        """
        Fitness is the total route cost using the haversine distance.
        The GA should attempt to minimize the fitness; minimal fitness => best fitness
        """
        X_train, X_test, y_train, y_test = self.clf_model.split_test_data(self.test_size, self.is_fixed)

        for df in [X_train, X_test]:
            features_to_drop = set(df.columns.values) - set(chromosome)
            if(len(features_to_drop) > 0):
                for feature in list(features_to_drop):
                    del df[feature]

        self.clf_model.fit_and_predict(X_train, X_test, y_train)
        fitness = self.clf_model.get_f1_score(y_test)

        return [chromosome,fitness]


    ## initialize population for classifier optimization
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

    ## initialize population for feature optimization
    def initialize_population_features(self):
        """
        Initialize the population by creating self.population_size chromosomes.
        Each chromosome represents the index of the point in the points list.
        Sorts the population by fitness and adds it to the generations list.
        """
        my_population = []

        # Loop through creating chromosomes until we fill the population
        for chromosome in range(0, self.population_size):
            # Shuffle the list of points and calculate the fitness of the path which returns the [chromosme,fitness] ready to be added to the population
            my_population.append(self.calculate_fitness_features(self.random_sample_features()))     

        # Sort the population by fitness
        my_population.sort(key=lambda x: x[1])

        self.generations.append(my_population)

    # Takes the index to the generation to repopulate from, and repopulates for classifier optimization
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

    # Takes the index to the generation to repopulate from, creates a new population of feature vectors
    def repopulate_features(self, gen, random_selection, num_features_to_change):
        """
        Creates a new generation by repopulation based on the previous generation.
        Calls selection, crossover, and mutate to create a child chromosome. Calculates fitness
        and continues until the population is full. Sorts the population by fitness
        and adds it to the generations list.
        """
        ## Ensure you keep the best of the best from the previous generation
        retain = math.ceil(self.population_size*0.025)
        new_population = self.generations[gen-1][:retain]
        if num_features_to_change != 0:
            for feature in range(0,abs(num_features_to_change)):
                if num_features_to_change > 0:
                    if len(new_population[0][0]) == 50:
                        break
                    for chromosome in new_population:
                        mutant_features = set(self.clf_model.X.columns.values) - set(chromosome[0])
                        random.shuffle(list(mutant_features))
                        chromosome[0].append(mutant_features.pop())
                else:
                    if len(new_population[0][0]) == 3:
                        break
                    for chromosome in new_population:
                        random.shuffle(chromosome[0])
                        chromosome[0].pop()


        ## Conduct selection, reproduction, and mutation operations to fill the rest of the population
        while len(new_population) < self.population_size:
            # Select the two parents from the growing population
            parent1, parent2 = self.selection(gen, random_selection)
            child = self.crossover_features(parent1, parent2)
            # Generate a random number, if it falls beneath the mutation_rate, mutate!!!!
            if (random.random() < self.mutation_rate):
                child = self.mutate_features(child)
                
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
            factor = 0.25	# Select from top %
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

    def crossover_features(self, parent1, parent2):
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
        # Step through each item in the chromosome and randomly choose which
        #  parent's genetic material to select
        for feature in parent1:
            value = None
            if random.randint(0,1) == 0:
                value = feature
            else:
                value = feature
            child.append(value)

        return self.calculate_fitness_features(child)


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

    def mutate_features(self, chromosome, num_mutations=3):
        """
        Choose a param and reset it with a randomized value
        """
        # Copy the child
        mutant_child = deepcopy(chromosome[0])
        
        for i in range(0,num_mutations):
            if len(mutant_child) == 50:
                random.shuffle(mutant_child)
                mutant_child.pop()

            # Get the features not in the chromosome already
            mutant_features = list(set(self.clf_model.X.columns.values) - set(mutant_child))
            mutant_child.remove(random.choice(mutant_child))
            mutant_child.append(random.choice(mutant_features))

        return self.calculate_fitness_features(mutant_child)

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

        return self.generations[self.num_generations-1][0]

    # Modified to rake a crossover strategy and random_selection flag (defaulted to False)
    def run_ga_features(self):
        """
        Initialize and repopulate until you have reached the maximum generations
        """
        self.initialize_population_features()

        for gen in range(self.num_generations-1):      #Note, you already ran generation 1
            self.repopulate_features(gen+1, self.rand_selection, random.randint(-7,7))
            print(f"Starting generation {gen+1}")
            if (gen + 1) % self.display_rate == 0:
                print("Best Feature Set for Gen:") # Print the generation, and the best (lowest) fitness score in the population for that generation
                print(self.generations[gen][0])
                print("Fitness Score")
                print(f"{round(self.generations[gen][0][1],3)*100}%")

        return self.generations[self.num_generations-1][0]