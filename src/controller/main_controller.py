"""
Authors: Marko Njegomir sw-38-2018
         Milos Popovic  sw-24-2018
"""
from PySide2.QtCore import QObject

class MainController(QObject):
    def __init__(self, app):
        super().__init__()

        self._app = app
        self.input_layout = self._app.main_window.centerWidget.layout().inputs_layout
        self.output_layout = self._app.main_window.centerWidget.layout().output_layout

    def add_console_iter(self, i, pop, maxf=False):
        best = pop.get_individuals()[0]
        fitness = best.get_fitness()
        if maxf:
            fitness *= -1
        # out = "Iteration " + str(i) + "| Fitness: " + str(fitness) + " Axis: [" + str(best.get_genes())
        out = "Iteration {:<4} | Fitness: {:<30} Axis: {}".format(i, fitness, str(best.get_genes()))
        # self.output_layout.clear_console()
        self.output_layout.append_output(out)

    def clear_console(self, value):
        self.output_layout.clear_console()

    def update_progress_bar(self, i, value):
        self.output_layout.set_progress_bar(value)
        self.set_comment("{} Iteration".format(i))

    def set_comment(self, text):
        self.output_layout.set_run_comment(text)

    def print_result(self, ind, maxf):
        fitness = ind.get_fitness()
        if maxf:
            fitness *= -1
        out = "\nResult:\n"
        out += "Fitness: {}\n".format(fitness)
        out += "Axis: {}".format(ind.get_genes())
        self.output_layout.append_output(out)
