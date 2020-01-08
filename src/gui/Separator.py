from PySide2.QtWidgets import QFrame

"""
Link: https://stackoverflow.com/questions/5671354/how-to-programmatically-make-a-horizontal-line-in-qt
Credits: https://stackoverflow.com/users/594173/michael-leonard
"""


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
