from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QWidget, QScrollArea

from src.gui.center.inputs_layout import InputsLayout
from src.gui.center.output_layout import OutputLayout


class CenterLayout(QGridLayout):
    def __init__(self):
        super(CenterLayout, self).__init__()

        self.inputs_widget = QWidget()
        self.inputs_layout = InputsLayout()
        self.inputs_widget.setLayout(self.inputs_layout)
        # self.inputs_widget.setStyleSheet("background:#eee")
        self.input_scroll_wrap = QScrollArea()
        self.input_scroll_wrap.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.input_scroll_wrap.setFixedWidth(self.inputs_widget.sizeHint().width())
        self.input_scroll_wrap.setWidget(self.inputs_widget)

        self.output_widget = QWidget()
        self.output_layout = OutputLayout()
        self.output_widget.setLayout(self.output_layout)
        # self.output_widget.setStyleSheet("background:#eee")

        self.tmpWidget2 = QWidget()
        # self.tmpWidget2.setStyleSheet("background:gray")

        # self.addWidget(InputsLayout, 1,1,1,1)
        self.addWidget(self.input_scroll_wrap, 1, 1, 1, 1)
        self.addWidget(self.output_widget, 1, 2, 1, 1)

        # connecting a signal that caries the output message with the print_output function
        # self.output_layout.ga_result.connect(self.output_layout.print_output)
        # self.inp_similarity_cb.stateChanged.connect(self.inp_similarity_cb)
