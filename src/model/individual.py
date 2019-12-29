from random import random
from src.functions.functions import ackley, griewank, michalewicz

class Individual(object):

    def __init__(self, num_genes, lower_bond, upper_bond):
        self._lower_bond = lower_bond
        self._upper_bond = upper_bond
        self._genes = self.make_genes(num_genes)
        self._fitness = None

    def make_genes(self, num_genes):
        genes = []
        for i in range(num_genes):
            genes.append(random() * (self._upper_bond - self._lower_bond) + self._lower_bond)
        return genes

    def get_genes(self):
        return self._genes

    def get_lower_bond(self):
        return self._lower_bond

    def get_upper_bond(self):
        return self._upper_bond

    def get_num_of_genes(self):
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

    def __str__(self):
        return str(self._genes)
