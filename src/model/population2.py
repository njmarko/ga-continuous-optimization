from math import ceil, sqrt
from random import sample, random, randint

from src.model.individual import Individual


class Population(object):

    def __init__(self, num_individuals, num_genes, lower_bound, upper_bound, fnc, individuals=None):
        self._num_individuals = num_individuals
        self._num_genes = num_genes
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._function = fnc
        if individuals:
            self._individuals = individuals
        else:
            self._individuals = self.make_population(num_individuals)
        self._parents = []
        self._elites = []
        self._fitness = []
        self._children = []
        self._mutated = []
        self._normalised_fitness = []
        self._cumulative_sum = []
        self.prepare_population()

    def get_elites(self):
        return self._elites

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

    def make_population(self, num_individuals):
        individuals = []
        for i in range(num_individuals):
            individuals.append(Individual(self._num_genes, self._lower_bound, self._upper_bound))
        return individuals

    def prepare_population(self):
        self.calculate_fitness()
        self.sort_individuals()

    def sort_individuals(self, individuals=None):
        if not individuals:
            self._individuals = sorted(self._individuals)
            self._fitness = sorted(self._fitness)
            return self._individuals
        else:
            return sorted(individuals)

    def separate_elites(self, elite_count=0.02):
        self.sort_individuals()
        num = ceil(elite_count * self.get_pop_size())  # at least one is elite
        for i in range(num):
            self._elites.append(self._individuals[i])

        return self._elites

    def calculate_fitness(self):
        self._fitness = []
        for i in range(len(self._individuals)):
            self._fitness.append(self._individuals[i].calc_fitness(self._function))
        return self._fitness

    def fitness_scaling(self, scaling_factor=-1, offset=0.001):
        highest = max(self._fitness)
        self._fitness = [scaling_factor * x + abs(highest) + offset for x in self._fitness]
        return self._fitness

    def rank_scaling(self):
        self._fitness = [1 / sqrt(x + 1) for x in range(len(self._fitness))]
        return self._fitness

    def calculate_normalized_fitness(self, fitness_remapping="Rank Scaling"):
        """
        Calculates normalised fitness for min of a function
        If the fitness value is closer to the minimum, normalized value will be greater
        This type of normalization is done so the individual with the lowest fitness value can
        take up range that is inversely proportional in size when creating cumulative fitness
        for roulette wheel selection
        :return:
        """

        self._normalised_fitness = []
        if fitness_remapping == "Fitness Scaling":
            self.fitness_scaling()
        elif fitness_remapping == "Rank Scaling":
            self.rank_scaling()
        fitness_sum = sum(self._fitness)
        for i in range(len(self._fitness)):
            self._normalised_fitness.append(self._fitness[i] / fitness_sum)
        self._normalised_fitness = sorted(self._normalised_fitness, reverse=True)
        return self._normalised_fitness

    def calculate_cumulative_sum(self):

        previous = 0
        self._cumulative_sum = []
        for i in (range(len(self._normalised_fitness))):
            self._cumulative_sum.append(previous + self._normalised_fitness[i])
            previous += self._normalised_fitness[i]
        return self._cumulative_sum

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

    def selection(self, method='Roulette Wheel', elite_count=0.02, fitness_remapping="Rank Scaling"):
        self.separate_elites(elite_count)
        chosen = []
        if method == 'Roulette Wheel':
            self.calculate_normalized_fitness(fitness_remapping)
            self.calculate_cumulative_sum()
            selected_indices = []
            while len(selected_indices) <= self.get_pop_size() - len(self._elites):
                selected_indices.append(self.roulette(random()))
            for index in sorted(selected_indices):
                chosen.append(self._individuals[index])
        elif method == 'Fittest Half':
            chosen = self._individuals[len(self._elites):self.get_pop_size() // 2 + len(self._elites)]
        elif method == 'Random':
            for i in range(self.get_pop_size() - len(self._elites)):
                position = randint(len(self._elites), self.get_pop_size() - 1)
                chosen.append(self._individuals[position])
        elif method == "Whole Population":
            for i in range(len(self._elites), self.get_pop_size()):
                chosen.append(self._individuals[i])
        self._parents = chosen
        return chosen

    def pairing(self, method='Random', crossover_fraction=0.8, crossover="Two point",
                intermediate_offset=0.2, fitness_remapping="Rank Scaling"):

        parents = self._elites + self._parents
        max_num = crossover_fraction * self._num_individuals
        children = []
        if method == 'Fittest':
            self.sort_individuals(parents)
            i = 0
            while len(children) < max_num - len(self._elites):
                if i + 1 >= len(parents):
                    i = 0
                new_children = parents[i].crossover(parents[i + 1], method=crossover, param1=intermediate_offset)
                children += new_children
                i += 2

        elif method == 'Random':
            while len(children) < max_num - len(self._elites):
                chosen = sample(range(0, len(parents)), 2)
                new_children = parents[chosen[0]].crossover(parents[chosen[1]], method=crossover,
                                                            param1=intermediate_offset)
                children += new_children
        elif method == "Roulette Wheel":
            self.calculate_normalized_fitness(fitness_remapping)
            self.calculate_cumulative_sum()
            self.sort_individuals(parents)
            selected_indices = [0 for i in range(2)]
            while len(children) < max_num - len(self._elites):
                selected_indices[0] = self.roulette(random()) % len(parents)
                selected_indices[1] = self.roulette(random()) % len(parents)
                while selected_indices[0] == selected_indices[1]:
                    selected_indices[1] = self.roulette(random()) % len(parents)
                new_children = parents[selected_indices[0]].crossover(parents[selected_indices[1]], method=crossover,
                                                                      param1=intermediate_offset)
                children += new_children

        self._children = children
        return children

    def mutations(self, method='Gauss', mutate_intensity=1):

        max_iter = self._num_individuals - len(self._children) - len(self._elites)
        mutated = []
        num = ceil(len(self._parents))
        positions = sample(range(0, len(self._parents)), num)
        i = 0
        while len(mutated) < max_iter:
            self._parents[positions[i]].mutation(method=method, mutate_intensity=mutate_intensity)
            mutated.append(self._parents[positions[i]])
            i += 1
            if i >= len(positions):
                i = 0
        self._mutated = mutated
        return mutated

    def finalize(self, create_new_gen=True):
        new_pop = self._elites + self._children + self._mutated
        if create_new_gen:
            pop = Population(self._num_individuals, self._num_genes, self._lower_bound, self._upper_bound,
                             self._function, new_pop)
            return pop
        else:
            self._elites = []
            self._children = []
            self._parents = []
            return self

    def __str__(self):
        string = ""
        for ind in self._individuals:
            string += str(ind) + "\n"
        return string
