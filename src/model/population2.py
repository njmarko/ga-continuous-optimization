from math import ceil
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

    def add_elites(self, elites):
        self._elites += elites
        self._elites = sorted(self._elites)

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
            # self.calculate_fitness()
            self._individuals = sorted(self._individuals)
            self._fitness = sorted(self._fitness)
            return self._individuals
        else:
            # self.calculate_fitness(individuals)
            return sorted(individuals)

    def separate_elites(self, elite_count=0.02, individuals=None):
        if not individuals:
            self.sort_individuals()
            num = ceil(elite_count * self.get_pop_size())  # at least one is elite
            for i in range(num):
                self._elites.append(self._individuals.pop(0))
                self._fitness.pop(0)
            return self._elites
        else:
            self.sort_individuals(individuals)
            num = ceil(elite_count * len(individuals))
            elites = []
            for i in range(num):
                elites.append(individuals.pop(0))
            return elites

    def calculate_fitness(self, individuals=None, function=None):
        if not function:
            function = self._function
        if not individuals:
            individuals = self._individuals
            fitness = self._fitness
        else:
            fitness = []
        for i in range(len(individuals)):
            fitness.append(individuals[i].calc_fitness(function))
        return fitness

    def fitness_scaling(self, fitness=None, scaling_factor=-1, offset=0.001):
        if not fitness:
            fitness = self._fitness
        highest = max(fitness)
        return [scaling_factor * x + abs(highest) + offset for x in fitness]

    def calculate_normalized_fitness(self, fitness=None, fitness_remapping="Fitness Scaling"):
        """
        Calculates normalised fitness for min of a function
        If the fitness value is closer to the minimum, normalized value will be greater
        This type of normalization is done so the individual with the lowest fitness value can
        take up range that is inversely proportional in size when creating cumulative fitness
        for roulette wheel selection
        :return:
        """
        if not fitness:
            fitness = self._fitness
        normalized = []
        if fitness_remapping == "Fitness Scaling":
            fitness = self.fitness_scaling(fitness)
        fitness_sum = sum(fitness)
        for i in range(len(fitness)):
            normalized.append(fitness[i] / fitness_sum)
        normalized = sorted(normalized, reverse=True)
        self._normalised_fitness = normalized
        return normalized

    def calculate_cumulative_sum(self, normalized_fitness=None):
        if not normalized_fitness:
            normalized_fitness = self._normalised_fitness
        previous = 0
        cumulative_sum = []
        for i in (range(len(normalized_fitness))):
            cumulative_sum.append(previous + normalized_fitness[i])
            previous += normalized_fitness[i]
        self._cumulative_sum = cumulative_sum
        return cumulative_sum

    def roulette(self, chance, cumulative_sum=None):
        if not cumulative_sum:
            cumulative_sum = self._cumulative_sum
        ind1 = 0
        ind2 = len(cumulative_sum) - 1
        mid = (ind1 + ind2) // 2
        while ind1 != mid and ind2 != mid:
            if cumulative_sum[mid] > chance:
                ind2 = mid
                mid = (ind1 + ind2) // 2
            else:
                ind1 = mid
                mid = (ind1 + ind2) // 2
        if chance >= cumulative_sum[mid]:
            return mid + 1
        else:
            return mid

    def selection(self, method='Roulette Wheel', elite_count=0.02, individuals=None):
        # self.calculate_fitness(individuals)
        # self.sort_individuals(individuals)
        self.separate_elites(elite_count, individuals)
        fitness = self._fitness
        chosen = []
        if method == 'Roulette Wheel':
            norm_fitness = self.calculate_normalized_fitness(fitness)
            self.calculate_cumulative_sum(norm_fitness)
            selected_indices = []
            while len(selected_indices) < self.get_pop_size() - len(self._elites):
                selected_indices.append(self.roulette(random()))
            for index in sorted(selected_indices):
                chosen.append(self._individuals[index])

        elif method == 'Fittest Half':
            chosen = self._individuals[0:self.get_pop_size() // 2]

        elif method == 'Random':
            for i in range(self.get_pop_size() - len(self._elites)):
                position = randint(0, self.get_pop_size() - len(self._elites))
                chosen.append(self._individuals[position])
        elif method == 'No Selection':
            chosen = self._individuals
        self._parents = chosen
        return chosen

    def pairing(self, method='Random', crossover_fraction=0.8, crossover="Two point", parents=None):
        if not parents:
            parents = self._elites + self._parents
            max_num = crossover_fraction * self._num_individuals
        else:
            max_num = crossover_fraction * len(parents)
        children = []
        if method == 'Fittest':
            self.sort_individuals(parents)
            i = 0
            while len(children) < max_num - len(self._elites):
                if i+1 >= len(parents):
                    i = 0
                new_children = parents[i].crossover(parents[i + 1], method=crossover)
                children += new_children
                i += 2

        elif method == 'Random':
            while len(children) < max_num - len(self._elites):
                chosen = sample(range(0, len(parents)), 2)
                new_children = parents[chosen[0]].crossover(parents[chosen[1]], method=crossover)
                children += new_children
        self._children = children
        return children

    def mutations(self, mutate_fraction=0.2, method='Gauss', parents=None):
        if not parents:
            parents = self._parents
            fraction = 1
            max_iter = self._num_individuals - len(self._children) - len(self._elites)
        else:
            fraction = mutate_fraction
            max_iter = ceil(fraction * len(parents))
        mutated = []
        num = ceil(fraction * len(parents))
        positions = sample(range(0, len(parents)), num)
        for i in range(max_iter):
            parents[positions[i]].mutation(method=method)
            mutated.append(parents[positions[i]])

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
