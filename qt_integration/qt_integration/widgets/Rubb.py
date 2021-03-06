import sys
import bpy

from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *

class Rubb(QLabel):
    def __init__(self,parent=None, view_settings = None):
        super(Rubb,self).__init__(parent)
        self.screenshot = None
        self.view_settings = view_settings
        self.parent = parent
        self.createWidgets()
        # install event filter
        self.fullScreenLabel.installEventFilter(self)


    def eventFilter(self,widget,event):
        if widget != self.fullScreenLabel:
            return QtGui.QLabel.eventFilter(self, widget, event)
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                #close full screen win
                self.fullScreenLabel.close()
            if event.button() == QtCore.Qt.LeftButton:
                self.leftMousePress = True
                self.origin = event.pos()

                if not self.rubberBand:
                    self.rubberBand = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,self.fullScreenLabel)
                self.rubberBand.setGeometry(QtCore.QRect(self.origin,QtCore.QSize()))
                self.rubberBand.show()
                return True
        if event.type() == QtCore.QEvent.MouseMove:

            if self.leftMousePress:
                if self.rubberBand:
                    size = event.pos().y()-self.origin.y()
                    self.rubberBand.setGeometry(self.origin.x(),self.origin.y(),size,size)
                    #self.rubberBand.setGeometry(QtCore.QRect(self.origin,event.pos()).normalized())
                return True
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.leftMousePress = False
            if self.rubberBand:
                #self.termination = event.pos()
                size = event.pos().y()-self.origin.y()
                #self.rect = QtCore.QRect(self.origin,self.termination)
                #self.screenshot = self.fullScreenPixmap.copy(self.rect.x(),self.rect.y(),self.rect.width(),self.rect.height())
                self.screenshot = self.fullScreenPixmap.copy(self.origin.x(),self.origin.y(),size,size)
                self.screenshot.scaled(256, 256)
                # save

                self.parent.exportAnimPanel.previewImage = QLabel()


                #thumb = QPixmap(thumb_path)
                #self.previewImage = QLabel()

                self.parent.exportAnimPanel.previewImage.setPixmap(self.screenshot)
                self.parent.exportAnimPanel.previewImage.setStyleSheet("border : none;")

                self.parent.exportAnimPanel.previewImage.setScaledContents(True)
                self.parent.exportAnimPanel.previewImageLayout.addWidget(self.parent.exportAnimPanel.previewImage)

                #restore_view_settings
                if self.view_settings :
                    bpy.context.user_preferences.themes['Default'].view_3d.space.gradients.high_gradient = self.view_settings['bg_color']

                    for index,area in enumerate(bpy.context.window_manager.windows[0].screen.areas) :
                        if index in self.view_settings['VIEW_3D']:
                            only_render = self.view_settings['VIEW_3D'][index][0]
                            world = self.view_settings['VIEW_3D'][index][1]

                            area.spaces[0].show_only_render = only_render
                            area.spaces[0].show_world = world

                self.fullScreenLabel.close()
                self.fullScreenLabel.removeEventFilter(self)

            return True
        return False

    def returnPixmap (self):
        return self.screenshot

    def createWidgets(self):
        self.fullScreenLabel = QLabel()
        self.fullScreenLabel.setCursor(QtCore.Qt.CrossCursor)

        self.fullScreenLabel.setAutoFillBackground(True)

        self.shotScreenLabel = QLabel()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self.fullScreenLabel)
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Highlight,QtGui.QBrush(QtCore.Qt.red))
        self.rubberBand.setPalette(pal)

        self.leftMousePress = False

        app = QApplication.primaryScreen()

        self.fullScreenPixmap = app.grabWindow(QApplication.desktop().winId())
        self.fullScreenLabel.setPixmap(self.fullScreenPixmap)

        self.fullScreenLabel.showFullScreen()

"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # your file path
    main=Rubb('D:/screenshot01')
    main.fullScreenLabel.show()
    app.exec_()"""
