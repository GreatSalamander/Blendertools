from PyQt5.QtWidgets import QListWidget,QListView
from PyQt5.QtCore import QSize
from ..functions import get_css,icon_path

import os

from .. import settings

class ThumbnailList(QListWidget):
    def __init__(self,folder):
        super().__init__()

        self.folder = folder
        self.setStyleSheet(get_css('ThumbnailList'))
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setWrapping(True)
        self.setIconSize(QSize(128, 128))
        self.setMovement(QListView.Static)

    def createWidget(self) :
        pass
