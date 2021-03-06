"""
Authors: Marko Njegomir sw-38-2018
         Milos Popovic  sw-24-2018
"""
# from PyQt5.QtWidgets import QComboBox
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFormLayout, QHBoxLayout, QCheckBox, QDoubleSpinBox, QComboBox, QRadioButton, QLabel, \
    QSpinBox

from src.functions.functions import ackley, griewank, michalewicz
from src.gui.Separator import QHLine


class InputsLayout(QFormLayout):
    # this signal is connected to print_output from output_layout class. Connection is done in center_layout
    ga_result = Signal(str)  # a signal that is emitted so it can transfer resulting string to the output_layout class

    def __init__(self):
        super(InputsLayout, self).__init__()
        self.big_font = QFont()
        self.medium_font = QFont()
        self.header = QLabel()
        self.header_general = QLabel()
        self.header_fitness_remapping = QLabel()
        self.header_stop = QLabel()
        self.header_selection = QLabel()
        self.header_pairing = QLabel()
        self.header_crossover = QLabel()
        self.header_mutation = QLabel()

        self.inp_functions_combo = QComboBox()
        self.inp_num_variables = QSpinBox()
        self.inp_extrema_min = QRadioButton("Minimum")
        self.inp_extrema_max = QRadioButton("Maximum")
        self.inp_pop_size = QSpinBox()
        self.inp_lower_bound = QDoubleSpinBox()
        self.inp_upper_bound = QDoubleSpinBox()
        # Stopping
        self.inp_max_iter = QSpinBox()
        self.inp_similarity_cb = QCheckBox()
        self.inp_similarity = QSpinBox()
        self.inp_best_result_cb = QCheckBox()
        self.inp_best_result = QDoubleSpinBox()
        self.inp_average_result_cb = QCheckBox()
        self.inp_average_result = QDoubleSpinBox()
        # Fitness remapping
        self.inp_fitness_remapping = QComboBox()
        # Selection
        self.inp_selection_method = QComboBox()
        self.inp_elitism = QDoubleSpinBox()
        # Pairing
        self.inp_pairing_method = QComboBox()
        # Crossover
        self.inp_crossover_method = QComboBox()
        self.inp_crossover_fraction = QDoubleSpinBox()
        self.intermediate_offset = QDoubleSpinBox()
        # Mutation
        self.inp_mutation_method = QComboBox()
        self.inp_mutation_intensity = QDoubleSpinBox()
        self.inp_mutation_intensity_final = QDoubleSpinBox()

        self.init_fonts()
        self.init_header()
        self.init_row_functions()
        self.init_row_general()
        self.init_row_fitness_remapping()
        self.init_row_stop()
        self.init_row_selection()
        self.init_row_pairing()
        self.init_row_crossover()
        self.init_row_mutation()

    def init_fonts(self):
        self.big_font.setPointSizeF(14)
        self.medium_font.setPointSizeF(12)

    def init_header(self):
        self.header.setFont(self.big_font)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setText("Genetic Algorithm Continuous Optimization")
        self.addRow(self.header)
        self.addRow(QHLine())

    def init_row_functions(self):
        self.inp_functions_combo.addItem("Ackley", ackley)
        self.inp_functions_combo.addItem("Griewank", griewank)
        self.inp_functions_combo.addItem("Michalewicz", michalewicz)

        self.inp_extrema_min.setChecked(True)

        radio_box = QHBoxLayout()
        radio_box.addWidget(self.inp_extrema_min)
        radio_box.addWidget(self.inp_extrema_max)
        self.addRow("Function:", self.inp_functions_combo)
        self.inp_num_variables.setMaximum(10000)
        self.inp_num_variables.setValue(10)
        self.addRow("Number of variables:", self.inp_num_variables)
        self.addRow("Find:", radio_box)
        self.addRow(QHLine())

    def init_row_general(self):
        self.header_general.setFont(self.medium_font)
        self.header_general.setText("General")

        self.inp_pop_size.setMaximum(10000)
        self.inp_pop_size.setValue(300)
        self.inp_lower_bound.setMaximum(1000000)
        self.inp_lower_bound.setMinimum(-1000000.0)
        self.inp_lower_bound.setValue(-10)
        self.inp_upper_bound.setMaximum(1000000)
        self.inp_upper_bound.setMinimum(-1000000.0)
        self.inp_upper_bound.setValue(10)

        self.addRow(self.header_general)
        self.addRow("Population size", self.inp_pop_size)
        self.addRow("Lower Bound", self.inp_lower_bound)
        self.addRow("Upper Bound", self.inp_upper_bound)
        self.addRow(QHLine())

    def init_row_fitness_remapping(self):
        self.header_fitness_remapping.setFont(self.medium_font)
        self.header_fitness_remapping.setText("Fitness Remapping")

        self.inp_fitness_remapping.addItem("Rank Scaling", "Rank Scaling")
        self.inp_fitness_remapping.addItem("Fitness Scaling", "Fitness Scaling")

        self.addRow(self.header_fitness_remapping)
        self.addRow("Fitness remapping", self.inp_fitness_remapping)
        self.addRow(QHLine())

    def init_row_stop(self):
        self.header_stop.setFont(self.medium_font)
        self.header_stop.setText("Stopping Criteria")

        self.inp_max_iter.setMaximum(100000)
        self.inp_similarity.setMaximum(100000)
        self.inp_best_result.setMinimum(-100000)
        self.inp_best_result.setMaximum(100000)
        self.inp_average_result.setMinimum(-100000)
        self.inp_average_result.setMaximum(100000)

        self.inp_max_iter.setValue(500)
        self.inp_similarity.setValue(80)
        self.inp_best_result.setValue(-10)
        self.inp_average_result.setValue(-10000)

        self.inp_similarity_cb.setText("Similar Results")
        self.inp_best_result_cb.setText("Best Result")
        self.inp_average_result_cb.setText("Average Result")
        self.inp_similarity_cb.stateChanged.connect(self.cb_similarity_signal)
        self.inp_best_result_cb.stateChanged.connect(self.cb_best_result_signal)
        self.inp_average_result_cb.stateChanged.connect(self.cb_average_result_signal)

        self.inp_similarity_cb.setChecked(False)
        self.inp_best_result_cb.setChecked(False)
        self.inp_average_result_cb.setChecked(False)

        self.inp_similarity.setEnabled(True)
        self.inp_best_result.setEnabled(False)
        self.inp_best_result.setStyleSheet("background:#555")
        self.inp_average_result.setEnabled(False)
        self.inp_average_result.setStyleSheet("background:#555")

        self.addRow(self.header_stop)
        self.addRow("Max iter", self.inp_max_iter)
        self.addRow(self.inp_similarity_cb, self.inp_similarity)
        self.addRow(self.inp_best_result_cb, self.inp_best_result)
        self.addRow(self.inp_average_result_cb, self.inp_average_result)
        self.addRow(QHLine())

    def init_row_selection(self):
        self.header_selection.setFont(self.medium_font)
        self.header_selection.setText("Selection")

        self.inp_selection_method.addItem("Fittest Half", "Fittest Half")
        self.inp_selection_method.addItem("Roulette Wheel", "Roulette Wheel")
        self.inp_selection_method.addItem("Random", "Random")
        self.inp_selection_method.addItem("Whole Population", "Whole Population")
        self.inp_elitism.setMaximum(1)
        self.inp_elitism.setValue(0.01)
        self.inp_elitism.setSingleStep(0.01)

        self.addRow(self.header_selection)
        self.addRow("Selection Method", self.inp_selection_method)
        self.addRow("Elitism Percentage", self.inp_elitism)
        self.addRow(QHLine())

    def init_row_pairing(self):
        self.header_pairing.setFont(self.medium_font)
        self.header_pairing.setText("Pairing")

        self.inp_pairing_method.addItem("Random", "Random")
        self.inp_pairing_method.addItem("Roulette Wheel", "Roulette Wheel")
        self.inp_pairing_method.addItem("Fittest", "Fittest")


        self.addRow(self.header_pairing)
        self.addRow("Pairing Method", self.inp_pairing_method)
        self.addRow(QHLine())

    def init_row_crossover(self):
        self.header_crossover.setFont(self.medium_font)
        self.header_crossover.setText("Crossover")

        self.inp_crossover_method.addItem("Intermediate", "Intermediate")
        self.inp_crossover_method.addItem("Line Intermediate", "Line Intermediate")
        self.inp_crossover_method.addItem("Heuristic", "Heuristic")
        self.inp_crossover_method.addItem("One point", "One point")
        self.inp_crossover_method.addItem("Two point", "Two point")
        self.inp_crossover_method.addItem("Random", "Random")
        self.inp_mutation_method.setCurrentIndex(2)
        self.inp_crossover_fraction.setMaximum(1)
        self.inp_crossover_fraction.setValue(0.7)
        self.inp_crossover_fraction.setSingleStep(0.05)
        self.intermediate_offset.setMaximum(20)
        self.intermediate_offset.setValue(1.55)
        self.intermediate_offset.setSingleStep(0.05)

        self.addRow(self.header_crossover)
        self.addRow("Crossover Method", self.inp_crossover_method)
        self.addRow("Crossover Fraction", self.inp_crossover_fraction)
        self.addRow("Intermediate Offset", self.intermediate_offset)
        self.addRow(QHLine())

    def init_row_mutation(self):
        self.header_mutation.setFont(self.medium_font)
        self.header_mutation.setText("Mutation")

        self.inp_mutation_method.addItem("Gauss", "Gauss")
        self.inp_mutation_method.addItem("Random", "Random")
        self.inp_mutation_intensity.setMaximum(200)
        self.inp_mutation_intensity.setValue(2)
        self.inp_mutation_intensity.setDecimals(4)

        self.inp_mutation_intensity.setSingleStep(0.01)
        self.inp_mutation_intensity_final.setMaximum(200)
        self.inp_mutation_intensity_final.setDecimals(4)
        self.inp_mutation_intensity_final.setValue(0.001)
        self.inp_mutation_intensity_final.setSingleStep(0.5)

        self.addRow(self.header_mutation)
        self.addRow("Mutation Method", self.inp_mutation_method)
        self.addRow("Mutation Intensity", self.inp_mutation_intensity)
        self.addRow("Final Mutation Intensity", self.inp_mutation_intensity_final)
        self.addRow(QHLine())

    def get_options(self):
        function = self.inp_functions_combo.currentData()
        num_var = self.inp_num_variables.text()
        if self.inp_extrema_min.isChecked():
            extrem = 0
        else:
            extrem = 1
        pop_size = self.inp_pop_size.text()
        low_bound = self.inp_lower_bound.text()
        upp_bound = self.inp_upper_bound.text()
        max_iter = self.inp_max_iter.text()
        sim_results = self.inp_similarity.text()
        best_res = self.inp_best_result.text()
        average_res = self.inp_average_result.text()
        select_method = self.inp_selection_method.currentText()
        elite_percent = self.inp_elitism.text()
        pairing = self.inp_pairing_method.currentText()
        crossover_method = self.inp_crossover_method.currentText()
        crossover_fraction = self.inp_crossover_fraction.text()
        intermediate_offset = self.intermediate_offset.text()
        mutation_method = self.inp_mutation_method.currentText()
        mutation_intensity = self.inp_mutation_intensity.text()
        mutation_intensity_final = self.inp_mutation_intensity_final.text()
        fitness_remapping = self.inp_fitness_remapping.currentText()

        options = {
            "function": function,
            "num_var": num_var,
            "pop_size": int(pop_size),
            "max_iter": int(max_iter),
            "lower_bound": float(low_bound.replace(",", ".")),
            "upper_bound": float(upp_bound.replace(",", ".")),
            "find_max": extrem,
            "prints": 0,
            "average_result": float(average_res.replace(",", ".")),
            "best_result": float(best_res.replace(",", ".")),
            "similarity": float(sim_results.replace(",", ".")),
            "selection": select_method,
            "pairing": pairing,
            "crossover": crossover_method,
            "crossover_fraction": float(crossover_fraction.replace(",", ".")),
            "intermediate_offset": float(intermediate_offset.replace(",", ".")),
            # 0 mean child will be between parents, 1 mean offset is same as two parent distance
            "mutation": mutation_method,
            "mutation_intensity": float(mutation_intensity.replace(",", ".")),
            "mutation_intensity_final": float(mutation_intensity_final.replace(",", ".")),
            "elitism": float(elite_percent.replace(",", ".")),
            "fitness_remapping": fitness_remapping
        }

        if not self.inp_similarity_cb.isChecked():
            options["similarity"] = None
        if not self.inp_best_result_cb.isChecked():
            options["best_result"] = None
        if not self.inp_average_result_cb.isChecked():
            options["average_result"] = None
        return options

    def cb_similarity_signal(self):
        if self.inp_similarity_cb.isChecked():
            self.inp_similarity.setEnabled(True)
            self.inp_similarity.setStyleSheet("")
        else:
            self.inp_similarity.setEnabled(False)
            self.inp_similarity.setStyleSheet("background:#555")

    def cb_best_result_signal(self):
        if self.inp_best_result_cb.isChecked():
            self.inp_best_result.setEnabled(True)
            self.inp_best_result.setStyleSheet("")
        else:
            self.inp_best_result.setEnabled(False)
            self.inp_best_result.setStyleSheet("background:#555")

    def cb_average_result_signal(self):
        if self.inp_average_result_cb.isChecked():
            self.inp_average_result.setEnabled(True)
            self.inp_average_result.setStyleSheet("")
        else:
            self.inp_average_result.setEnabled(False)
            self.inp_average_result.setStyleSheet("background:#555")
