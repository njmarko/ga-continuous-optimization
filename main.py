import sys

from src.functions.functions import *
from src.ga import ga
from src.controller.main_controller import MainController
from src.gui.main_window import MainWindow
from PySide2.QtWidgets import QApplication


def main():
    main_app = QApplication(sys.argv)
    main_app.main_window = MainWindow()
    main_app.main_window.show()
    main_app.setStyle('fusion')
    main_app.controller = MainController(main_app)
    sys.exit(main_app.exec_())


if __name__ == '__main__':
    main()
