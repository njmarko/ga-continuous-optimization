from PySide2.QtWidgets import QFormLayout, QLineEdit, QComboBox


class InputsLayout(QFormLayout):
    def __init__(self):
        super(InputsLayout, self).__init__()

        self.inp1 = QLineEdit()
        self.combo = QComboBox()
        self.combo.addItem("Element")

        self.addRow("Input1: ", self.inp1)
        self.addRow("Function", self.combo)
        # self.addItem(self.inp1)
        # self.addItem(self.combo)
