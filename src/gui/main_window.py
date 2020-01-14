from PySide2.QtWidgets import QMainWindow, QDockWidget, QWidget

from src.gui.center_layout import CenterLayout


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.tree = None
        self.centerWidget = QWidget()
        self.centerWidget.setLayout(CenterLayout())

        self.setCentralWidget(self.centerWidget)
        self.setWindowTitle("GA")
        self.leftDock = QDockWidget(QWidget())
        self.setStyleSheet("QWidget{background: #444; color: #ddd;}"
                           "QScrollBar{background:#383838; width:5px;}"
                           "QScrollBar::handle { background: #353535; border-radius: 10px;}")
        # self.actionManager = QApplication.instance().actionManager

        self.setDocumentMode(False)
        self.setMinimumSize(500, 400)
        self.resize(1024, 768)
