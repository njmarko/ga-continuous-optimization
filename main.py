from src.model.individual import Individual
from src.model.population import Population
from src.functions.functions import ackley


def main():
    pop = Population(50, 2, -10, 10, ackley)

    for i in range(200):
        print(pop)
        print(pop.get_pop_size())
        pop = pop.selection()
        pop.pairing()
        pop.mutations()
        print(pop.get_pop_size())
    print(pop)



if __name__ == '__main__':
    main()
