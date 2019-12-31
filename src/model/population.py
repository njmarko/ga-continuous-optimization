from math import ceil
from random import sample, random

from src.model.individual import Individual


class Population(object):

    def __init__(self, num_individuals, num_genes, lower_bound, upper_bound, fnc, parents=None):
        self._num_individuals = num_individuals
        self._num_genes = num_genes
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._function = fnc
        if parents:
            self._individuals = []
            self._parents = parents
        else:
            self._individuals = self.make_population(num_individuals)
            self._parents = []
        self._elites = []
        self._fitness = []
        self._normalised_fitness = []
        self._cumulative_sum = []
        self._selected = []
        self._children = []

    def add_elites(self, elites):
        self._elites += elites
        self._elites = sorted(self._elites)

    def get_elites(self):
        return self._elites

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

    def get_pop_size(self):
        return len(self._individuals)

    def get_fitness(self):
        return self._fitness

    def get_normalized_fitness(self):
        return self._normalised_fitness

    def get_cumulative_sum(self):
        return self._cumulative_sum

    def get_function(self):
        return self._function

    def sort_individuals(self):
        self.calculate_fitness()
        self._individuals = sorted(self._individuals)

    def separate_elites(self, elite_count=0.02):
        self.sort_individuals()
        num = ceil(elite_count * self.get_pop_size())  # at least one is elite
        for i in range(num):
            self._elites.append(self._individuals.pop(0))

    def calculate_fitness(self):
        self._fitness = []
        for i in range(self.get_pop_size()):
            self._fitness.append(self._individuals[i].calc_fitness(self._function))

    def calculate_normalized_fitness(self):
        normalized = []
        fitness_sum = sum(self._fitness)
        for i in range(self.get_pop_size()):
            normalized.append(self._fitness[i] / fitness_sum)
        self._normalised_fitness = sorted(normalized)

    def calculate_cumulative_sum(self):
        previous = 0
        for i in reversed(range(self.get_pop_size())):
            self._cumulative_sum.append(previous + self._normalised_fitness[i])
            previous += self._normalised_fitness[i]

    def get_min(self):
        try:
            return min(self._fitness)
        except ValueError:
            return None

    def get_max(self):
        try:
            return max(self._fitness)
        except ValueError:
            return None

    def get_average(self):
        return sum(self._fitness) / self._num_genes

    def roulette(self, chance):
        ind1 = 0
        ind2 = len(self._cumulative_sum) - 1
        mid = (ind1 + ind2) // 2
        while ind1 != mid and ind2 != mid:
            if self._cumulative_sum[mid] > chance:
                ind2 = mid
                mid = (ind1 + ind2) // 2
            else:
                ind1 = mid
                mid = (ind1 + ind2) // 2
        if chance >= self._cumulative_sum[mid]:
            return mid + 1
        else:
            return mid

    def selection(self, method='Roulette Wheel', elitism=True):
        self.sort_individuals()
        if elitism:
            self.separate_elites()
        selected = None
        if method == 'Roulette Wheel':
            self.calculate_fitness()
            self.calculate_normalized_fitness()
            self.calculate_cumulative_sum()
            selected_indices = set()
            while len(selected_indices) < self.get_pop_size() // 2:
                selected_indices.add(self.roulette(random()))
            chosen = []
            for index in sorted(selected_indices):
                chosen.append(self._individuals[index])
            selected = Population(self.get_pop_size() + len(self._elites), self._num_genes, self._lower_bound,
                                  self._upper_bound, self._function, chosen)
        elif method == 'Fittest Half':
            chosen = self._individuals[0:self.get_pop_size() // 2]
            selected = Population(self.get_pop_size() + len(self._elites), self._num_genes,
                                  self._lower_bound,
                                  self._upper_bound, self._function, chosen)
        elif method == 'Random':
            chosen = []
            positions = sample(range(self.get_pop_size()), self.get_pop_size() // 2)
            for i in positions:
                chosen.append(self._individuals[i])
            selected = Population(self.get_pop_size() + len(self._elites), self._num_genes,
                                  self._lower_bound,
                                  self._upper_bound, self._function, chosen)
        selected.add_elites(self.get_elites())
        # selected.calculate_fitness()
        return selected

    def pairing(self, method='Fittest', crossover_fraction=0.8, crossover="Two point", elitism=True):
        if elitism:
            self._parents = self._elites + self._parents
        max_num = crossover_fraction * self._num_individuals
        if method == 'Fittest':
            self.sort_individuals()
            i = 0
            while len(self._children) < max_num - len(self._elites):
                children = self._parents[i].crossover(self._parents[i + 1], method=crossover)
                self._children += children
                i += 1
        elif method == 'Random':
            while len(self._children) < max_num - len(self._elites):
                chosen = sample(range(0, len(self._parents)), 2)
                children = self._parents[chosen[0]].crossover(self._parents[chosen[1]], method=crossover)
                self._children += children

    def mutations(self, mutate_fraction=0.8, method='Gauss', elitism=True):
        if elitism:
            self._parents = self._parents[len(self._elites):]  # so elites don't mutate
        self._individuals += self._children + self._parents
        num = ceil(mutate_fraction * len(self._individuals))
        positions = sample(range(0, len(self._individuals)), num)
        for pos in positions:
            self._individuals[pos].mutation(method=method)
        self.finalize()

    def finalize(self):
        self.sort_individuals()
        self._individuals = self._individuals[:self._num_individuals - len(self._elites)]
        self._individuals = self._elites + self._individuals
        self.sort_individuals()
        self._elites = []
        self._children = []
        self._parents = []

    def __str__(self):
        string = ""
        for ind in self._individuals:
            string += str(ind) + "\n"
        return string
