from src.functions.functions import ackley
from src.ga import ga


def main():
    options = {
        "pop_size": 100,
        "max_iter": 200,
        "lower_bound": -10,
        "upper_bound": 10,
        "find_max": 0,
        "prints": 1,
        "average_result": None,
        "best_result": None,
        "similarity": 60
    }
    ga(ackley, 2, options)


if __name__ == '__main__':
    main()
