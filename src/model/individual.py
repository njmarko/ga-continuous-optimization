"""
Authors: Marko Njegomir sw-38-2018
         Milos Popovic  sw-24-2018
"""
from random import random, randint, gauss, sample

from src.functions.functions import ackley, griewank, michalewicz


class Individual(object):

    def __init__(self, num_genes, lower_bound, upper_bound, genes=None):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        if genes:
            self._genes = genes
        else:
            self._genes = self.make_genes(num_genes)
        self._fitness = None

    def make_genes(self, num_genes):
        genes = []
        for i in range(num_genes):
            genes.append(random() * (self._upper_bound - self._lower_bound) + self._lower_bound)
        return genes

    def __eq__(self, other):
        return self._fitness == other.get_fitness()

    def __ge__(self, other):
        return self._fitness >= other.get_fitness()

    def __le__(self, other):
        return self._fitness <= other.get_fitness()

    def __lt__(self, other):
        return self._fitness < other.get_fitness()

    def __gt__(self, other):
        return self._fitness > other.get_fitness()

    def get_fitness(self):
        return self._fitness

    def get_genes(self):
        return self._genes

    def set_genes(self, genes):
        self._genes = genes

    def get_lower_bond(self):
        return self._lower_bound

    def get_upper_bond(self):
        return self._upper_bound

    def get_num_of_genes(self):
        return len(self._genes)

    def gene_length(self):
        return len(self._genes)

    def calc_fitness(self, fnc):
        self._fitness = fnc(self._genes)
        return self._fitness

    # Optional
    def calc_fitness_ackley(self):
        return self.calc_fitness(ackley)

    def calc_fitness_griewank(self):
        return self.calc_fitness(griewank)

    def calc_fitness_michalewicz(self):
        return self.calc_fitness(michalewicz)

    # -----------

    def mutation(self, method="Gauss", mutate_intensity=1):
        new_mutated = Individual(self.get_num_of_genes(), self.get_lower_bond(), self.get_upper_bond(),
                                 self.get_genes()[:])

        if method == "Gauss":
            for i in range(self.get_num_of_genes()):
                new_mutated._genes[i] = \
                    self._genes[i] + gauss(0, mutate_intensity)

        elif method == "Random":
            lower_bound = self.get_lower_bond()
            upper_bound = self.get_upper_bond()
            for i in range(self.get_num_of_genes()):
                new_mutated._genes[i] = random() * (upper_bound - lower_bound) + lower_bound

        return new_mutated

    def crossover(self, other, method="Two point", param1=1):
        size = self.gene_length()
        genes1 = []
        genes2 = []
        if method == "Two point":
            if size == 1:
                method = "One point"
            else:
                genes1, genes2 = self.crossover_two_point(other)
                return Individual(size, self._lower_bound, self._upper_bound, genes1), Individual(size,
                                                                                                  self._lower_bound,
                                                                                                  self._upper_bound,
                                                                                                  genes2)

        if method == "One point":
            genes1, genes2 = self.crossover_one_point(other)

        elif method == "Random":
            genes1, genes2 = self.crossover_random(other)

        elif method == "Intermediate":
            genes1, genes2 = self.crossover_intermediate(other, param1)

        elif method == "Line Intermediate":
            genes1, genes2 = self.crossover_line_intermediate(other, param1)

        elif method == "Heuristic":
            genes1, genes2 = self.crossover_heuristic(other, param1)

        else:
            print(method)
            print("No crossover, random values for children")

        return Individual(size, self._lower_bound, self._upper_bound, genes1), Individual(size, self._lower_bound,
                                                                                          self._upper_bound, genes2)

    def crossover_one_point(self, other):
        point1 = randint(0, self.gene_length() - 1)

        genes1 = self.get_genes()[0:point1] + other.get_genes()[point1:]
        genes2 = other.get_genes()[0:point1] + self.get_genes()[point1:]
        return genes1, genes2

    def crossover_two_point(self, other):
        positions = sorted(sample(range(0, self.gene_length()), 2))

        point1 = positions[0]
        point2 = positions[1]

        genes1 = self.get_genes()[0:point1] + other.get_genes()[point1:point2] + self.get_genes()[point2:]
        genes2 = other.get_genes()[0:point1] + self.get_genes()[point1:point2] + other.get_genes()[point2:]
        return genes1, genes2

    def crossover_random(self, other):
        genes1 = []
        genes2 = []
        for i, j in zip(self.get_genes(), other.get_genes()):
            if random() > 0.5:
                genes1.append(i)
                genes2.append(j)
            else:
                genes1.append(j)
                genes2.append(i)
        return genes1, genes2

    def crossover_intermediate(self, other, param1):
        ratio1 = []
        ratio2 = []

        for i in range(self.get_num_of_genes()):
            ratio1.append(random() * param1)
            ratio2.append(random() * param1)

        genes1 = []
        genes2 = []
        for i in range(self.get_num_of_genes()):
            genes1.append(self.get_genes()[i] + ratio1[i] * (other.get_genes()[i] - self.get_genes()[i]))
            genes2.append(self.get_genes()[i] + ratio2[i] * (other.get_genes()[i] - self.get_genes()[i]))
        # a = -param1
        # b = 1 + param1
        # genes1 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
        #           for i, rand in enumerate([uniform(a, b) for _ in range(self.get_num_of_genes())])]
        # genes2 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
        #           for i, rand in enumerate([uniform(a, b) for _ in range(self.get_num_of_genes())])]
        return genes1, genes2

    def crossover_line_intermediate(self, other, param1):
        ratio1 = param1 * random()
        ratio2 = param1 * random()

        genes1 = []
        genes2 = []
        for i in range(self.get_num_of_genes()):
            genes1.append(self.get_genes()[i] + ratio1 * (other.get_genes()[i] - self.get_genes()[i]))
            genes2.append(self.get_genes()[i] + ratio2 * (other.get_genes()[i] - self.get_genes()[i]))
        # a = -param1
        # b = 1 + param1
        #
        # rand = uniform(a, b)
        # genes1 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
        #           for i in range(self.get_num_of_genes())]
        # rand = uniform(a, b)
        # genes2 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
        #           for i in range(self.get_num_of_genes())]
        return genes1, genes2

    def crossover_heuristic(self, other, param1):
        ind1 = self.get_genes()
        ind2 = other.get_genes()
        if self.get_fitness() < other.get_fitness():
            ind1, ind2 = ind2, ind1

        ratio1 = []
        ratio2 = []

        for i in range(self.get_num_of_genes()):
            ratio1.append(random() * param1)
            ratio2.append(random() * param1)

        genes1 = []
        genes2 = []
        for i in range(self.get_num_of_genes()):
            genes1.append(ind1[i] + ratio1[i] * (ind2[i] - ind1[i]))
            genes2.append(ind1[i] + ratio2[i] * (ind2[i] - ind1[i]))
        return genes1, genes2

    def __str__(self):
        return "Fitness: " + str(self._fitness) + " " + str(self._genes)
