from PyQt5.QtWidgets import QComboBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFormLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QRadioButton, QLabel, QSpinBox

from src.functions.functions import ackley, michalewicz, griewank
from src.gui.Separator import QHLine


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
        self.inp_lower_bound = QSpinBox()
        self.inp_upper_bound = QSpinBox()
        # Stopping
        self.inp_max_iter = QSpinBox()
        self.inp_similarity = QSpinBox()
        self.inp_best_result = QSpinBox()
        self.inp_average_result = QSpinBox()
        # Selection
        self.inp_selection_method = QComboBox()
        self.inp_elitism = QSpinBox()
        # Pairing
        self.inp_pairing_method = QComboBox()
        # Crossover
        self.inp_crossover_method = QComboBox()
        self.inp_crossover_fraction = QSpinBox()
        self.intermediate_offset = QSpinBox()
        # Mutation
        self.inp_mutation_method = QComboBox()
        self.inp_mutation_intensity = QSpinBox()

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

        self.addRow(self.header_general)
        self.addRow("Population size", self.inp_pop_size)
        self.addRow("Lower Bound", self.inp_lower_bound)
        self.addRow("Upper Bound", self.inp_upper_bound)
        self.addRow(QHLine())

    def init_row_stop(self):
        self.header_stop.setFont(self.medium_font)
        self.header_stop.setText("Stopping Criteria")

        self.addRow(self.header_stop)
        self.addRow("Max iter", self.inp_max_iter)
        self.addRow("Similar Results", self.inp_similarity)
        self.addRow("Best Result", self.inp_best_result)
        self.addRow("Average Result", self.inp_average_result)
        self.addRow(QHLine())

    def init_row_selection(self):
        self.header_selection.setFont(self.medium_font)
        self.header_selection.setText("Selection")

        self.addRow(self.header_selection)
        self.addRow("Selection Method", self.inp_selection_method)
        self.addRow("Elitism Percentage", self.inp_elitism)
        self.addRow(QHLine())

    def init_row_pairing(self):
        self.header_pairing.setFont(self.medium_font)
        self.header_pairing.setText("Pairing")

        self.addRow(self.header_pairing)
        self.addRow("Pairing Method", self.inp_pairing_method)
        self.addRow(QHLine())

    def init_row_crossover(self):
        self.header_crossover.setFont(self.medium_font)
        self.header_crossover.setText("Crossover")

        self.addRow(self.header_crossover)
        self.addRow("Crossover Method", self.inp_crossover_method)
        self.addRow("Crossover Fraction", self.inp_crossover_fraction)
        self.addRow("Intermediate Offset", self.intermediate_offset)
        self.addRow(QHLine())

    def init_row_mutation(self):
        self.header_mutation.setFont(self.medium_font)
        self.header_mutation.setText("Mutation")

        self.addRow(self.header_mutation)
        self.addRow("Mutation Method", self.inp_mutation_method)
        self.addRow("Mutation Intensity", self.inp_mutation_intensity)
        self.addRow(QHLine())

    def init_row_run(self):
        self.header_run.setFont(self.medium_font)
        self.header_run.setText("RUN")

        self.addRow(self.header_run)
        self.addRow(self.btn_run)
