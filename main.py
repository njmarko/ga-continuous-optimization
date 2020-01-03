from src.functions.functions import ackley, griewank, michalewicz
from src.ga import ga
from src.model.population2 import Population


def main():
    options = {
        "pop_size": 100,
        "max_iter": 200,
        "lower_bound": 0,
        "upper_bound": 4,
        "find_max": 0,
        "prints": 1,
        "average_result": None,
        "best_result": None,
        "similarity": 60,
        "selection": "Roulette Wheel",
        "pairing": "Fittest",
        "crossover": "Two point",
        "crossover_fraction": 0.8,
        "mutation": "Gauss",
        "mutate_fraction": 0.2,
        "elitism": True
    }
    ga(michalewicz, 2, options)
    print("Pravi optimum za michalewicz(dim=2): " + str(michalewicz([2.20, 1.57])))  # ovo je optimum za 2 promenljive


if __name__ == '__main__':
    main()
