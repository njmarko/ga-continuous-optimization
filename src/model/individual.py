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
            old_genes = self.get_genes()
            for i in rand_id:
                self._genes[i] = \
                    self._genes[i] + gauss(0, lower_bond)

        elif method == "random":
            for i in rand_id:
                self._genes[i] = random() * (upper_bond - lower_bond) + lower_bond

        return self._genes

    def __str__(self):
        return str(self._genes)
