from PyQt5.QtWidgets import QLineEdit
from ..functions import get_css

class LineEdit(QLineEdit) :
    def __init__(self):
        super().__init__()
        self.setStyleSheet(get_css('LineEdit'))
        self.createWidget()

    def createWidget(self) :
        pass
