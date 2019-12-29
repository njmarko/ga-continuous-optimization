from src.model.individual import Individual
from random import random, randint
from copy import deepcopy


class Population(object):

    def __init__(self, num_individuals, num_genes, lower_bound, upper_bound, fnc, individuals=None):
        self._num_genes = num_genes
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        if individuals:
            self._individuals = individuals
        else:
            self._individuals = self.make_population(num_individuals)
        self._fitness = []
        self._normalised_fitness = []
        self._cumulative_sum = []
        self._function = fnc

    def make_population(self, num_individuals):
        individuals = []
        for i in range(num_individuals):
            individuals.append(Individual(self._num_genes, self._lower_bound, self._upper_bound))
        return individuals

    def get_individuals(self):
        return self._individuals

    def get_num_genes(self):
        return self._num_genes

    def get_lower_bound(self):
        return self._lower_bound

    def get_upper_bound(self):
        return self._upper_bound

    def get_population_size(self):
        return len(self._individuals)

    def get_fitness(self):
        return self._fitness

    def get_normalized_fitness(self):
        return self._normalised_fitness

    def get_cumulative_sum(self):
        return self._cumulative_sum

    def get_function(self):
        return self._function

    def calculate_fitness(self):
        for i in range(self.get_population_size()):
            self._fitness.append(self._individuals[i].calc_fitness(self._function))

    def calculate_normalized_fitness(self):
        normalized = []
        fitness_sum = sum(self._fitness)
        for i in range(self.get_population_size()):
            normalized.append(self._fitness[i] / fitness_sum)
        self._normalised_fitness = sorted(normalized, reverse=True)

    def calculate_cumulative_sum(self):
        previous = 0
        for i in reversed(range(self.get_population_size())):
            self._cumulative_sum.append(previous + self._normalised_fitness[i])
            previous += self._normalised_fitness[i]

    # def roulette(self, cumulative_sum, chance):
    #     var = list(cumulative_sum.copy())
    #     var.append(chance)
    #     var = sorted(var)
    #     return var.index(chance)

    def selection(self, method='Fittest Half'):
        self.calculate_fitness()
        self.calculate_normalized_fitness()
        self.calculate_cumulative_sum()
        selected = None
        if method == 'Roulette Wheel':
            selected_indices = []
        #     for i in range(self.get_population_size() // 2):
        #         selected_indices.append(self.roulette(self._cumulative_sum, random()))
        #         while len(set(selected_indices)) != len(selected_indices):
        #             selected_indices[i] = (self.roulette(self._cumulative_sum, random()))
        #     chosen = []
        #     print(selected_indices)
        #     for index in sorted(selected_indices):
        #         chosen.append(self._individuals[index])
        #     selected = Population(self.get_population_size() // 2, self._num_genes, self._lower_bound,
        #                           self._upper_bound, self._function, chosen)
        elif method == 'Fittest Half':
            chosen = self._individuals[0:self.get_population_size() // 2]
            selected = Population(self.get_population_size() // 2, self._num_genes, self._lower_bound,
                                  self._upper_bound, self._function, chosen)
        elif method == 'Random':
            chosen = []
            for i in range(self.get_population_size() // 2):
                num = randint(1, self.get_population_size() // 2)
                chosen.append(self._individuals[num])
            selected = Population(self.get_population_size() // 2, self._num_genes, self._lower_bound,
                                  self._upper_bound, self._function, chosen)
        selected.calculate_fitness()
        return selected
