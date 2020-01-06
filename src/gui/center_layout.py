from PySide2.QtWidgets import QGridLayout, QWidget

from src.gui.center.inputs_layout import InputsLayout
from src.gui.center.output_layout import OutputLayout


class CenterLayout(QGridLayout):
    def __init__(self):
        super(CenterLayout, self).__init__()

        self.inputs_widget = QWidget()
        self.inputs_widget.setLayout(InputsLayout())
        self.inputs_widget.setStyleSheet("background:#eee")

        self.output_widget = QWidget()
        self.output_widget.setLayout(OutputLayout())
        self.output_widget.setStyleSheet("background:#eee")

        self.tmpWidget2 = QWidget()
        self.tmpWidget2.setStyleSheet("background:gray")

        # self.addWidget(InputsLayout, 1,1,1,1)
        self.addWidget(self.inputs_widget, 1, 1, 1, 1)
        self.addWidget(self.output_widget, 1, 2, 1, 1)
