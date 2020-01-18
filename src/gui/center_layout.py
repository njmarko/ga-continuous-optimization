"""
Authors: Marko Njegomir sw-38-2018
         Milos Popovic  sw-24-2018
"""
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
        self.input_scroll_wrap = QScrollArea()
        self.input_scroll_wrap.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.input_scroll_wrap.setFixedWidth(self.inputs_widget.sizeHint().width())
        self.input_scroll_wrap.setWidget(self.inputs_widget)

        self.output_widget = QWidget()
        self.output_layout = OutputLayout()
        self.output_widget.setLayout(self.output_layout)

        self.tmpWidget2 = QWidget()

        self.addWidget(self.input_scroll_wrap, 1, 1, 1, 1)
        self.addWidget(self.output_widget, 1, 2, 1, 1)
