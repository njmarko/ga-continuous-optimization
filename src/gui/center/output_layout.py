from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGridLayout, QApplication, QTextEdit, QWidget, QLabel, QVBoxLayout, QProgressBar, \
    QPushButton

from src.ga import ga


class OutputLayout(QGridLayout):
    ga_result = Signal(str)  # a signal that is emited so it can transfer resulting string to the output_layout class

    def __init__(self):
        super(OutputLayout, self).__init__()
        self.run_section = QWidget()
        self.run_section.setMaximumHeight(100)
        self.run_layout = QVBoxLayout()
        self.header_run = QLabel()
        self.run_comment = QLabel()
        self.btn_run = QPushButton("Run")
        self.btn_run.clicked.connect(self.run_button_clicked)

        self.progress = QProgressBar()
        self.console = QTextEdit()
        self.console.setText("This is output")
        self.init_console()
        self.init_run_section()

        self.addWidget(self.console, 1, 1, 1, 1)

    def print_output(self, output_text):
        self.console.setText(output_text)

    def append_output(self, text):
        self.console.append(text)

    def init_console(self):
        # new_font = QFont('courier new', 8)
        # self.console.setFont(new_font)
        self.console.setReadOnly(True)
        self.console.horizontalScrollBar().setEnabled(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)

    def init_run_section(self):
        font14 = QFont()
        font14.setPointSizeF(12)
        self.header_run.setFont(font14)
        self.header_run.setText("RUN")
        self.run_comment.setText("Iteration stopped in 128 iteration")
        self.run_comment.hide()
        font10 = QFont()
        font10.setPointSizeF(10)
        self.run_comment.setFont(font10)
        self.run_comment.setAlignment(Qt.AlignCenter)
        self.progress.show()

        self.addWidget(self.header_run, 2, 1, 1, 1)
        self.addWidget(self.run_comment, 3, 1, 1, 1)
        self.addWidget(self.progress, 4, 1, 1, 1)
        self.addWidget(self.btn_run, 5, 1, 1, 1)

    def run_button_clicked(self):
        self.clear_console()
        options = QApplication.instance().main_window.centerWidget.layout().inputs_layout.get_options()
        controller = QApplication.instance().controller
        self.progress.show()
        function = options["function"]
        num_var = options["num_var"]

        res = ga(function, int(num_var), options, controller)
        # self.ga_result.emit(str(res))  # emits a string representation of the best individual

    def set_progress_bar(self, value):
        self.progress.setValue(value)

    def set_status_text(self, text):
        self.run_comment.setText(text)

    def clear_console(self):
        self.console.clear()

    def set_run_comment(self, text):
        self.run_comment.setText(text)
        self.run_comment.show()
