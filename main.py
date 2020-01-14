import sys

from src.functions.functions import *
from src.ga import ga
from src.controller.main_controller import MainController
from src.gui.main_window import MainWindow
from PySide2.QtWidgets import QApplication


def main():
    main_app = QApplication(sys.argv)
    main_app.main_window = MainWindow()
    main_app.main_window.show()
    main_app.setStyle('fusion')
    main_app.controller = MainController(main_app)

    # options = {
    #     "pop_size": 100,
    #     "max_iter": 200,
    #     "lower_bound": -10,
    #     "upper_bound": 10,
    #     "find_max": 0,
    #     "prints": 0,
    #     "average_result": None,
    #     "best_result": None,
    #     "similarity": 60,
    #     "selection": "Roulette Wheel",
    #     "pairing": "Fittest",
    #     "crossover": "Intermediate",
    #     "crossover_fraction": 0.8,
    #     "intermediate_offset": 2,  # 0 mean child will be between parents, 1 mean offset is same as two parent distance
    #     "mutation": "Gauss",
    #     "mutate_fraction": 0.2,
    #     "elitism": 0.02
    # }
    # res = ga(ackley, 2, options)
    # # ga(ackley, 2, options)
    # # print("Pravi optimum za michalewicz(dim=2): " + str(michalewicz([2.20, 1.57])))  # ovo je optimum za 2 promenljive
    # print(res)
    # res = ga(ackley, 2, options)
    # print(res)
    # res = ga(ackley, 2, options)
    # print(res)
    # res = ga(ackley, 2, options)
    # print(res)
    # res = ga(ackley, 2, options)
    # print(res)

    sys.exit(main_app.exec_())


if __name__ == '__main__':
    main()
