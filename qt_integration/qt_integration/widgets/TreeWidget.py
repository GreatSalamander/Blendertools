from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem
from PyQt5.QtGui import QFont,QIcon
from ..functions import get_css,icon_path

import os

from .. import settings

class TreeWidget(QTreeWidget) :
    def __init__(self):
        super().__init__()
        self.header().close()
        self.setStyleSheet(get_css('TreeWidget'))
        self.folder = settings.ROOT
        self.setAlternatingRowColors(True)
        self.setIndentation(15)
        self.createWidget()

    def is_folder_in_path(self,path):
        for file in os.listdir(path) :
            full_path = os.path.join(path,file)
            if os.path.isdir(full_path) :
                return True
        return False

    def recursive_dir(self,path,item,starting_level) :
        for fileName in os.listdir(path) :
            full_path = os.path.join(path,fileName)
            level = full_path.count(os.sep)-starting_level
            if os.path.isdir(full_path) and self.is_folder_in_path(full_path) :
                if level == 1 :
                    font = QFont("Gill Sans",9)#QFont.Bold
                    icon = QIcon(icon_path('ICON_FOLDER'))
                else :
                    font = QFont("Gill Sans",10-level)
                    icon = QIcon(icon_path('ICON_SMALL_FOLDER'))

                name = QTreeWidgetItem(item, [fileName.title(),full_path])
                #name.setIcon(0,icon)
                name.setFont(0,font)
                #full_path = QTreeWidgetItem(item,[full_path])
                #item =
                self.recursive_dir(full_path,name,starting_level)

    def createWidget(self):
        #self.setStyleSheet(self.style_tree_view)
        #self.setStyleSheet("border: 10px solid #d9d9d9;")
        self.recursive_dir(self.folder,self,self.folder.count(os.sep))
