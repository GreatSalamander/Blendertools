from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QCompleter,QSpinBox,QSpacerItem,QCheckBox,QSizePolicy,QLabel,QFrame,QApplication
from PyQt5.QtCore import QStringListModel,Qt
from PyQt5.QtGui import QPixmap


from .PushButton import PushButton
from .LineEdit import LineEdit
from .Label import Label
from .SpinBox import SpinBox
from .CheckBox import CheckBox
from .Rubb import Rubb
from .TitleBar import TitleBar


from .. import settings

from ..functions import get_css,icon_path,store_anim,write_anim,clear_layout

import sys
import bpy
import os
import tempfile

class ExportAnimPanel(QVBoxLayout) :
    def __init__(self, parent=None):
        super().__init__(parent)

        self.previewImage = None
        self.parent = parent
        self.base_path = settings.ROOT
        self.screenshot = None
        self.createWidget()

    def createWidget(self) :
        #self.mainLayout = QVBoxLayout()
        self.setContentsMargins(12, 6, 6, 6)
        self.setSpacing(8)

        self.previewImagePanel = QFrame()
        self.previewImageLayout = QVBoxLayout()
        self.previewImagePanel.setLayout(self.previewImageLayout)
        self.previewImagePanel.setMinimumSize(230,230)
        self.previewImagePanel.setMaximumSize(230,230)
        #­self.previewImage.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.previewImagePanel.setStyleSheet("border-style : dashed;border-width : 2px; border-color:rgb(60,60,60);background-color : rgb(100,100,100);")
        self.previewImageLayout.setContentsMargins(0, 0, 0, 0)
        #self.previewImageLayout.setSpacing(0)

        # Action Name
        self.actionName = LineEdit()
        self.actionNameLayout = QHBoxLayout()
        self.actionNameLayout.addWidget(Label(text = 'Name :'))
        self.actionNameLayout.addWidget(self.actionName)

        # Category Name
        self.model = QStringListModel()
        self.model.setStringList(['pose','mains','expressions','cycle'])
        self.cat_completer = QCompleter()
        self.cat_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.cat_completer.setModel(self.model)

        self.categoryName = LineEdit()
        self.categoryName.setCompleter(self.cat_completer)
        self.categoryNameLayout = QHBoxLayout()

        self.categoryNameLayout.addWidget(Label(text='Category :'))
        self.categoryNameLayout.addWidget(self.categoryName)

        # Frame Range
        self.frameRangeLayout = QHBoxLayout()

        self.frameRangeIn = SpinBox()
        self.frameRangeIn.setValue(bpy.context.scene.frame_current)
        self.frameRangeIn.setMaximum(10000)
        self.frameRangeIn.valueChanged.connect(lambda : self.update_number())

        self.frameRangeOut = SpinBox()
        self.frameRangeOut.setValue(bpy.context.scene.frame_current)
        self.frameRangeOut.setMaximum(10000)
        self.frameRangeOut.valueChanged.connect(lambda : self.update_number())

        self.frameRangeLayout.addWidget(Label(text='Frame Range :'))
        self.frameRangeLayout.addWidget(self.frameRangeIn)
        self.frameRangeLayout.addWidget(self.frameRangeOut)

        #animation_step
        self.animationSettingsLayout = QHBoxLayout()
        self.step = SpinBox()
        self.step.setValue(2)
        self.step.setMinimum(1)
        self.step.valueChanged.connect(lambda : self.update_number())

        self.imgNumber = Label()
        self.imgNumber.setText(self.update_number())

        self.animationSettingsLayout.addWidget(Label(text='Step :'))
        self.animationSettingsLayout.addWidget(self.step)
        self.animationSettingsLayout.addWidget(Label(text='Number:'))
        self.animationSettingsLayout.addWidget(self.imgNumber)

        #option
        self.optionLayout = QHBoxLayout()
        self.only_selected = CheckBox('Selected Only')
        self.bezier = CheckBox('Bezier')
        self.mirror_pose = CheckBox('Mirror Pose')
        self.optionLayout.addWidget(self.only_selected)
        self.optionLayout.addWidget(self.bezier)
        self.optionLayout.addWidget(self.mirror_pose)

        # tools layout
        self.toolsLayout = QHBoxLayout()
        horizontalSpacer = QSpacerItem(128, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        verticalSpacer = QSpacerItem(20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.toolsLayout.addItem(horizontalSpacer)
        #thumbnail button
        self.btn_thumbnail = PushButton(icon = icon_path('ICON_RENDER_REGION'),size = [24,24])
        self.btn_thumbnail.clicked.connect(self.set_thumbnail)
        #ok_button
        self.btn_ok = PushButton(text = 'OK')
        self.btn_ok.clicked.connect(self.ok)
        #cancel_button
        self.btn_cancel = PushButton(text = 'Cancel')
        self.btn_cancel.clicked.connect(self.cancel)

        self.toolsLayout.addWidget(self.btn_thumbnail)
        self.toolsLayout.addWidget(self.btn_ok)
        self.toolsLayout.addWidget(self.btn_cancel)

        # Adding layout to main Widget
        self.addWidget(self.previewImagePanel)
        self.addLayout(self.actionNameLayout)
        self.addLayout(self.categoryNameLayout)
        self.addLayout(self.frameRangeLayout)
        self.addLayout(self.animationSettingsLayout)
        self.addLayout(self.optionLayout)
        self.addItem(verticalSpacer)
        self.addLayout(self.toolsLayout)


    def update_number(self) :
        img_frame = round((int(self.frameRangeOut.text()) - int(self.frameRangeIn.text())) / int(self.step.text()))

        self.imgNumber.setText(str(img_frame))



    def ok(self):
        path = os.path.join(self.base_path,self.asset,self.categoryName.text(),self.actionName.text())
        thumb_path = os.path.join(path,self.actionName.text()+'_thumbnail.jpg')

        action = store_anim(int(self.frameRangeIn.text()),int(self.frameRangeOut.text()),self.only_selected.isChecked(),self.bezier.isChecked(),self.mirror_pose.isChecked())

        write_anim(path,self.actionName.text(),action)

        description = open(os.path.join(path,self.actionName.text()+'_description.txt'),'w')

        if self.previewImage.pixmap() :
            self.previewImage.pixmap().save(thumb_path, 'jpg',75)


    def cancel(self):
        bar = TitleBar(parent = self.parent)
        TitleBar.show()
        ('print cancel')

    def show_completion(self) :
        self.setPopup(QAbstractItemView())


    def set_thumbnail(self) :
        active_ob = bpy.context.scene.objects.active
        clear_layout(self.previewImageLayout)

        '''
        #for all 3d view show only render set to true
        view_settings={}
        view_settings['VIEW_3D'] = {}
        view_settings['bg_color'] = bpy.context.user_preferences.themes['Default'].view_3d.space.gradients.high_gradient
        bpy.context.user_preferences.themes['Default'].view_3d.space.gradients.high_gradient = (0.5,0.5,0.5)

        for index,area in enumerate(bpy.context.window_manager.windows[0].screen.areas) :
            if area.type == 'VIEW_3D' :
                only_render = area.spaces[0].show_only_render
                world = area.spaces[0].show_world

                view_settings['VIEW_3D'][index] = [only_render,world]
                area.spaces[0].show_only_render = True
                area.spaces[0].show_world = True
        '''

        main = Rubb(parent = self.parent)
        main.fullScreenLabel.show()

        if active_ob and active_ob.type == 'ARMATURE' :
            if active_ob.proxy_group :
                self.asset = active_ob.proxy_group.name

            else :
                self.asset = active_ob.name
