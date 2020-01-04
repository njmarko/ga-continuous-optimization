from random import random, uniform, randint, gauss, sample

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

    # lower_bound je devijacija u gausu
    def mutation(self, chance=1, mutation_rate=2, method="Gauss", lower_bound=5, upper_bound=6):
        if random() > chance:
            return self._genes

        gene_len = self.gene_length()
        if mutation_rate > gene_len:
            mutation_rate = gene_len
        rand_id = sample(range(0, gene_len), mutation_rate)
        if method == "Gauss":
            for i in rand_id:
                self._genes[i] = \
                    self._genes[i] + gauss(0, 1)

        elif method == "Random":
            for i in rand_id:
                self._genes[i] = random() * (upper_bound - lower_bound) + lower_bound

        return self._genes

    def crossover(self, other, method="Two point", param1=1):
        size = self.gene_length()
        genes1 = []
        genes2 = []

        if method == "Two point":
            if size == 1:
                method = "One point"
            else:
                positions = sorted(sample(range(0, size), 2))

                point1 = positions[0]
                point2 = positions[1]

                genes1 = self.get_genes()[0:point1] + other.get_genes()[point1:point2] + self.get_genes()[point2:]
                genes2 = other.get_genes()[0:point1] + self.get_genes()[point1:point2] + other.get_genes()[point2:]

        if method == "One point":
            point1 = randint(0, size - 1)

            genes1 = self.get_genes()[0:point1] + other.get_genes()[point1:]
            genes2 = other.get_genes()[0:point1] + self.get_genes()[point1:]

        elif method == "Random":
            for i, j in zip(self.get_genes(), other.get_genes()):
                if random() > 0.5:
                    genes1.append(i)
                    genes2.append(j)
                else:
                    genes1.append(j)
                    genes2.append(i)

        # parent1 + RAND(0,1) * RATIO * (parent2-parent1)  ->  can't go before parent1
        # elif method == "Intermediate":
        #     ratio = 1
        #     genes1 = [other.get_genes()[i] + random() * ratio * (self.get_genes()[i] - other.get_genes()[i])
        #               for i in range(self.get_num_of_genes())]
        #     genes2 = [other.get_genes()[i] + random() * ratio * (self.get_genes()[i] - other.get_genes()[i])
        #               for i in range(self.get_num_of_genes())]

        elif method == "Intermediate":
            a = -param1
            b = 1 + param1
            genes1 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
                      for i, rand in enumerate([uniform(a, b) for _ in range(self.get_num_of_genes())])]
            genes2 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
                      for i, rand in enumerate([uniform(a, b) for _ in range(self.get_num_of_genes())])]

        # elif method == "Line Intermediate":
        #     ratio = 1
        #     rand = random()
        #     genes1 = [other.get_genes()[i] + rand * ratio * (self.get_genes()[i] - other.get_genes()[i])
        #               for i in range(self.get_num_of_genes())]
        #     rand = random()
        #
        #     genes2 = [other.get_genes()[i] + rand * ratio * (self.get_genes()[i] - other.get_genes()[i])
        #               for i in range(self.get_num_of_genes())]

        elif method == "Line Intermediate":
            a = -param1
            b = 1 + param1

            rand = uniform(a, b)
            genes1 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
                      for i in range(self.get_num_of_genes())]
            rand = uniform(a, b)
            genes2 = [other.get_genes()[i] * rand + self.get_genes()[i] * (1 - rand)
                      for i in range(self.get_num_of_genes())]

        elif method == "Heuristic":
            pass
        else:
            print("No crossover, random values for children")

        return Individual(size, self._lower_bound, self._upper_bound, genes1), Individual(size, self._lower_bound,
                                                                                          self._upper_bound, genes2)

    def __str__(self):
        return "Fitness: " + str(self._fitness) + " " + str(self._genes)
