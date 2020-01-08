# from PyQt5.QtWidgets import QComboBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFormLayout, QHBoxLayout, QPushButton, QDoubleSpinBox, QComboBox, QRadioButton, QLabel, QSpinBox
from src.functions.functions import ackley, michalewicz, griewank
from src.gui.Separator import QHLine
from src.ga import ga
from src.functions.functions import ackley,griewank,michalewicz

# class QHLine(QFrame):
#     def __init__(self):
#         super(QHLine, self).__init__()
#         self.setFrameShape(QFrame.HLine)
#         self.setFrameShadow(QFrame.Sunken)

class InputsLayout(QFormLayout):
    def __init__(self):
        super(InputsLayout, self).__init__()
        self.big_font = QFont()
        self.medium_font = QFont()
        self.header = QLabel()
        self.header_general = QLabel()
        self.header_stop = QLabel()
        self.header_selection = QLabel()
        self.header_pairing = QLabel()
        self.header_crossover = QLabel()
        self.header_mutation = QLabel()
        self.header_run = QLabel()

        self.inp_functions_combo = QComboBox()
        self.inp_extrema_min = QRadioButton("Minimum")
        self.inp_extrema_max = QRadioButton("Maximum")
        self.inp_pop_size = QSpinBox()
        self.inp_lower_bound = QDoubleSpinBox()
        self.inp_upper_bound = QDoubleSpinBox()
        # Stopping
        self.inp_max_iter = QSpinBox()
        self.inp_similarity = QSpinBox()
        self.inp_best_result = QDoubleSpinBox()
        self.inp_average_result = QDoubleSpinBox()
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

        self.btn_run = QPushButton("Run")

        self.init_fonts()
        self.init_header()
        self.init_row_functions()
        self.init_row_general()
        self.init_row_stop()
        self.init_row_selection()
        self.init_row_pairing()
        self.init_row_crossover()
        self.init_row_mutation()
        self.init_row_run()

        # connect buttons
        self.btn_run.clicked.connect(self.run_button_clicked)


    def init_fonts(self):
        self.big_font.setPointSizeF(14)
        self.medium_font.setPointSizeF(12)

    def init_header(self):
        self.header.setFont(self.big_font)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setText("Genetic Algorith Continuous Optimization")
        self.addRow(self.header)
        self.addRow(QHLine())

    def init_row_functions(self):
        self.inp_functions_combo.addItem("Ackley", ackley)
        self.inp_functions_combo.addItem("Griewank", griewank)
        self.inp_functions_combo.addItem("Michalewicz", michalewicz)

        self.inp_extrema_min.setChecked(True)

        # Is it okay to create object in function?
        radio_box = QHBoxLayout()
        radio_box.addWidget(self.inp_extrema_min)
        radio_box.addWidget(self.inp_extrema_max)
        self.addRow("Function:", self.inp_functions_combo)
        self.addRow("Find:", radio_box)
        self.addRow(QHLine())

    def init_row_general(self):
        self.header_general.setFont(self.medium_font)
        self.header_general.setText("General")

        self.inp_pop_size.setMaximum(10000)
        self.inp_pop_size.setValue(100)
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

    def init_row_stop(self):
        self.header_stop.setFont(self.medium_font)
        self.header_stop.setText("Stopping Criteria")

        self.inp_max_iter.setMaximum(100000)
        self.inp_similarity.setMaximum(100000)
        self.inp_best_result.setMinimum(-100000)
        self.inp_best_result.setMaximum(100000)
        self.inp_average_result.setMinimum(-100000)
        self.inp_average_result.setMaximum(100000)

        self.inp_max_iter.setValue(100)
        self.inp_similarity.setValue(60)
        # TODO: Checkbox for NONE value
        self.inp_best_result.setValue(-10)
        self.inp_average_result.setValue(0)

        self.addRow(self.header_stop)
        self.addRow("Max iter", self.inp_max_iter)
        self.addRow("Similar Results", self.inp_similarity)
        self.addRow("Best Result", self.inp_best_result)
        self.addRow("Average Result", self.inp_average_result)
        self.addRow(QHLine())

    def init_row_selection(self):
        self.header_selection.setFont(self.medium_font)
        self.header_selection.setText("Selection")

        self.inp_selection_method.addItem("Roulette Wheel", "Roulette Wheel")
        self.inp_selection_method.addItem("Fittest Half", "Fittest Half")
        self.inp_selection_method.addItem("Random", "Random")
        self.inp_selection_method.addItem("No Selection", "No Selection")
        self.inp_elitism.setMaximum(1)
        self.inp_elitism.setValue(0.05)

        self.addRow(self.header_selection)
        self.addRow("Selection Method", self.inp_selection_method)
        self.addRow("Elitism Percentage", self.inp_elitism)
        self.addRow(QHLine())

    def init_row_pairing(self):
        self.header_pairing.setFont(self.medium_font)
        self.header_pairing.setText("Pairing")

        self.inp_pairing_method.addItem("Fittest", "Fittest")
        self.inp_pairing_method.addItem("Random", "Random")

        self.addRow(self.header_pairing)
        self.addRow("Pairing Method", self.inp_pairing_method)
        self.addRow(QHLine())

    def init_row_crossover(self):
        self.header_crossover.setFont(self.medium_font)
        self.header_crossover.setText("Crossover")

        self.inp_crossover_method.addItem("Intermediate", "Intermediate")
        self.inp_crossover_method.addItem("Line Intermediate", "Line Intermediate")
        self.inp_crossover_method.addItem("One point", "One point")
        self.inp_crossover_method.addItem("Two point", "Two point")

        # TODO: Heuristic
        self.inp_crossover_method.addItem("Heuristic (TO DO)", "Heuristic")
        self.inp_crossover_method.addItem("Random", "Random")
        self.inp_mutation_method.setCurrentIndex(2)
        self.inp_crossover_fraction.setMaximum(1)
        self.inp_crossover_fraction.setValue(0.8)
        self.intermediate_offset.setMaximum(20)
        self.intermediate_offset.setValue(1.2)

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
        self.inp_mutation_intensity.setValue(1)

        self.addRow(self.header_mutation)
        self.addRow("Mutation Method", self.inp_mutation_method)
        self.addRow("Mutation Intensity", self.inp_mutation_intensity)
        self.addRow(QHLine())

    def init_row_run(self):
        self.header_run.setFont(self.medium_font)
        self.header_run.setText("RUN")

        self.addRow(self.header_run)
        self.addRow(self.btn_run)


    def run_button_clicked(self):

        function = self.inp_functions_combo.currentData()

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
        elit_percent = self.inp_elitism.text()
        pairing = self.inp_pairing_method.currentText()
        crossover_method = self.inp_crossover_method.currentText()
        crossover_fraction = self.inp_crossover_fraction.text()
        intermediate_offset = self.intermediate_offset.text()
        mutation_method = self.inp_mutation_method.currentText()
        mutation_intensity = self.inp_mutation_intensity.text()

        #za debug
        print(function)
        print(extrem)
        print(pop_size)
        print(low_bound)
        print(upp_bound)
        print(max_iter)
        print(sim_results)
        print(best_res)
        print(average_res)
        print(select_method)
        print(elit_percent)
        print(pairing)
        print(crossover_method)
        print(crossover_fraction)
        print(intermediate_offset)
        print(mutation_method)
        print(mutation_intensity)


        options = {
            "pop_size": int(pop_size),
            "max_iter": int(max_iter),
            "lower_bound": float(low_bound),
            "upper_bound": float(upp_bound),
            "find_max": extrem,
            "prints": 1,
            "average_result": float(average_res),
            "best_result": float(best_res),
            "similarity": float(sim_results),
            "selection": select_method,
            "pairing": pairing,
            "crossover": crossover_method,
            "crossover_fraction": float(crossover_fraction),
            "intermediate_offset": float(intermediate_offset),
            # 0 mean child will be between parents, 1 mean offset is same as two parent distance
            "mutation": mutation_method,
            "mutate_fraction": float(mutation_intensity),
            "elitism": float(elit_percent)
        }

        res = ga(function, 2, options)



