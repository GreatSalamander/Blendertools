from PyQt5.QtWidgets import QLabel
from ..functions import get_css

class Label(QLabel) :
    def __init__(self,text = None):
        super().__init__()
        self.text = text
        self.setStyleSheet(get_css('Label'))
        self.createWidget()

    def createWidget(self) :
        self.setText(self.text)
