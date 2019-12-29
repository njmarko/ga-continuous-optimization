from random import random, randint, gauss

from src.functions.functions import ackley, griewank, michalewicz


class Individual(object):

    def __init__(self, num_genes, lower_bound, upper_bound):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._genes = self.make_genes(num_genes)
        self._fitness = None

    def make_genes(self, num_genes):
        genes = []
        for i in range(num_genes):
            genes.append(random() * (self._upper_bound - self._lower_bound) + self._lower_bound)
        return genes

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

    # lower_bond je devijacija u gausu
    def mutation(self, mutation_rate=2, method="gauss", lower_bond=5, upper_bond=6):
        gene_len = self.gene_length()
        if mutation_rate > gene_len:
            print("ee")
            mutation_rate = gene_len
        rand_id = []
        while len(rand_id) < mutation_rate:
            rand = randint(0, gene_len - 1)
            if rand not in rand_id:
                rand_id.append(rand)

        if method == "gauss":
            for i in rand_id:
                self._genes[i] = \
                    self._genes[i] + gauss(0, lower_bond)

        elif method == "random":
            for i in rand_id:
                self._genes[i] = random() * (upper_bond - lower_bond) + lower_bond

        return self._genes

    def crossover(self, other, method="One Point"):
        size = self.gene_length()
        ind1 = Individual(size, 0, 0)
        ind2 = Individual(size, 0, 0)
        genes1 = []
        genes2 = []

        if method == "two point":
            if size == 1:
                method = "one point"
            else:
                point1 = randint(0, size)
                point2 = randint(0, size)
                while point1 == point2:
                    point2 = randint(0, size)

                genes1 = self.get_genes()[0:point1] + other.get_genes()[point1:point2] + self.get_genes()[point2:]
                genes2 = other.get_genes()[0:point1] + self.get_genes()[point1:point2] + other.get_genes()[point2:]

        if method == "one point":
            point1 = randint(0, size - 1)

            genes1 = self.get_genes()[0:point1] + other.get_genes()[point1:]
            genes2 = other.get_genes()[0:point1] + self.get_genes()[point1:]
            print("more")

        elif method == "random":
            for i, j in zip(self.get_genes(), other.get_genes()):
                if random() > 0.5:
                    genes1.append(i)
                    genes2.append(j)
                else:
                    genes1.append(j)
                    genes2.append(i)

        ind1.set_genes(genes1)
        ind2.set_genes(genes2)

        return [ind1, ind2]

    def __str__(self):
        return str(self._genes)
