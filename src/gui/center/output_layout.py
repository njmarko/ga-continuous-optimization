from PySide2.QtWidgets import QGridLayout, QTextEdit


class OutputLayout(QGridLayout):
    def __init__(self):
        super(OutputLayout, self).__init__()

        self.console = QTextEdit()
        self.console.setText("This is output")

        self.addWidget(self.console, 1, 1, 1, 1)

    def print_output(self, output_text):
        self.console.setText(output_text)
