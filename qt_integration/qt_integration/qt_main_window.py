import sys, logging, os
import bpy
import subprocess

from math import trunc

from PyQt5.QtWidgets import QWidget,QFrame,QVBoxLayout,QHBoxLayout,QSplitter,QSplitter,QShortcut,QSizePolicy,QListWidgetItem,QPlainTextEdit,QLabel
from PyQt5.QtCore import QDir,Qt,QSize
from PyQt5.QtGui import QIcon,QKeySequence,QPixmap

from .functions import set_thumbnail,store_anim,write_anim,read_anim,find_fcurve_path,icon_path,get_css,clear_layout
from .widgets import *

from qt_integration import settings

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.folder = settings.ROOT

        self.widget_close = None
        self.context = None

        self.base_path = os.path.dirname(__file__)
        #self.folder = folder

        QDir.setCurrent(self.base_path)


        #self.setWindowTitle('Data Library')
        #self.resize(840, 480)

        self.color_background = '#404040'
        self.color_text_field = '#A7A7A7'
        self.color_button = '#979797'
        self.color_panel_bright = '#727272'
        self.color_panel_dark = '#525252'
        self.color_border = '#2E2E2E'

        self.setUI()

        #self.style_button = "border-color: %s;background-color:%s;"%(self.color_border,self.color_button)

    def setUI(self):
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setStyleSheet(get_css("MainWindow"))

        #top Bar
        self.topBarArea = QFrame()
        self.topBarArea.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.topBarArea.setMinimumHeight(32)
        self.topBarArea.setMaximumHeight(32)

        self.topBarLayout = QHBoxLayout()
        self.topBarLayout.setSpacing(2)
        self.topBarLayout.setContentsMargins(4, 1, 4, 1)

        self.topBarArea.setLayout(self.topBarLayout)
        self.topBarArea.setStyleSheet(get_css('Bar'))

        #Left Panel
        self.leftPanel = QFrame()
        #self.leftPanel.setMaximumWidth(132)


        self.leftPanel.setStyleSheet(get_css('PanelLeft'))

        self.leftPanelLayout = QVBoxLayout()
        self.leftPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.leftPanel.setLayout(self.leftPanelLayout)

        self.outlinerLayout = QVBoxLayout()
        self.outlinerLayout.setContentsMargins(1, 5, 1, 1)

        self.assetChoiceLayout = QVBoxLayout()
        self.assetChoiceLayout.setContentsMargins(0, 0, 0, 0)

        self.treeWidget = TreeWidget()
        self.treeWidget.itemClicked.connect(self.onClickItem)

        # comboBox asset cbox_asset_choice
        self.cbox_asset_choice = ComboBox()
        self.cbox_asset_choice.setMinimumHeight(28)

        self.cbox_asset_choice.setStyleSheet(get_css("ComboBoxAsset"))

        #self.cbox_asset_choice.setStyleSheet("border-left : none; border-right : none; border-top : none")
        self.cbox_asset_choice.addItem(QIcon(icon_path("ICON_ACTION")), "Action")
        self.cbox_asset_choice.addItem(QIcon(icon_path("ICON_GROUP")), "Group")
        self.cbox_asset_choice.addItem(QIcon(icon_path("ICON_MATERIAL")), "Material")

        self.assetChoiceLayout.addWidget(self.cbox_asset_choice)
        self.outlinerLayout.addWidget(self.treeWidget)

        self.leftPanelLayout.addLayout(self.assetChoiceLayout)
        self.leftPanelLayout.addLayout(self.outlinerLayout)

        #Tool Box
        self.toolBoxPanel = QFrame()
        self.toolBoxPanel.setStyleSheet("border : none; background-color : rgb(100,100,100)")
        self.toolBoxLayout  = QVBoxLayout()

        self.toolBoxPanel.setLayout(self.toolBoxLayout)

        self.leftPanelLayout.addWidget(self.toolBoxPanel)

        #Middle
        self.middle = QFrame()
        self.middle.setStyleSheet(get_css('2DSpace'))

        self.middleLayout = QVBoxLayout()
        self.middleLayout.setContentsMargins(0, 0, 0, 0)

        self.thumbnailList = ThumbnailList(self.folder)
        self.thumbnailList.itemClicked.connect(self.onClickThumb)
        self.thumbnailList.itemDoubleClicked.connect(self.apply_pose)

        self.middleLayout.addWidget(self.topBarArea)
        self.middleLayout.addWidget(self.thumbnailList)

        self.middle.setLayout(self.middleLayout)


        #Right Panel
        self.rightPanel = QFrame()
        #self.rightPanel.setMaximumWidth(256)
        #self.rightPanel.setMinimumWidth(256)


        self.rightPanel.setStyleSheet(get_css('PanelRight'))

        self.rightLayout = QVBoxLayout()
        self.rightLayout.setContentsMargins(4, 4, 4, 4)

        self.rightPanel.setLayout(self.rightLayout)


        #Splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet(get_css('Splitter'))
        #self.splitter.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        ## Dir button
        btn_parent_dir = PushButton(icon= icon_path('ICON_FILE_PARENT'),size = [22,22])

        ### add_asset button
        btn_add_asset = PushButton(icon= icon_path('ICON_ZOOMIN'),size = [22,22])
        btn_add_asset.clicked.connect(self.exportAnimPanel)

        btn_refresh = PushButton(icon= icon_path('ICON_FILE_FOLDER'),size = [22,22])
        btn_refresh.clicked.connect(self.refresh)

        #open folder button
        btn_open_folder= PushButton(icon = icon_path('OPEN_FOLDER'),size = [22,22])
        btn_open_folder.clicked.connect(self.open_folder)

        #search bar
        self.search_bar = LineEdit()
        self.search_bar.textChanged.connect(self.filterThumbnail)

        self.topBarLayout.addWidget(btn_parent_dir)
        self.topBarLayout.addWidget(self.search_bar)
        self.topBarLayout.addWidget(btn_refresh)
        self.topBarLayout.addWidget(btn_open_folder)


        # Adding Panel to splitter
        self.splitter.addWidget(self.leftPanel)
        self.splitter.addWidget(self.middle)
        self.splitter.addWidget(self.rightPanel)

        self.splitter.setSizes([132,512,256])

        self.splitter.setStretchFactor(0,0)
        self.splitter.setStretchFactor(1,1)
        self.splitter.setStretchFactor(2,0)

        #self.mainLayout.addWidget(self.topBarArea)
        self.mainLayout.addWidget(self.splitter)

        #shortcut
        self.shortcut_zoom_in = QShortcut(QKeySequence("+"), self)
        self.shortcut_zoom_out = QShortcut(QKeySequence("-"), self)

        self.shortcut_zoom_in.activated.connect(self.zoom_in)
        self.shortcut_zoom_out.activated.connect(self.zoom_out)

        self.setLayout(self.mainLayout)
        #self.show()

    def refresh(self) :
        self.treeWidget.clear()

        TreeWidget().recursive_dir(self.folder,self.treeWidget,self.folder.count(os.sep))

    def open_folder(self) :
        try:
            os.startfile(self.folder)
        except:
            subprocess.Popen(['xdg-open', self.folder])

    def exportAnimPanel(self) :
        clear_layout(self.rightLayout)

        self.exportAnimPanel = ExportAnimPanel(self)

        self.rightLayout.addLayout(self.exportAnimPanel)


    def zoom_in(self) :
        new_size = self.thumbnailList.iconSize().width()
        if not new_size >512 :
            new_size*=1.25

        self.thumbnailList.setIconSize(QSize(new_size,new_size))
        #self.thumbnailList.setStyleSheet("QListView::item {height: %s;}"%(new_size+6))

    def zoom_out(self) :
        new_size = self.thumbnailList.iconSize().width()
        if not new_size <64 :
            new_size*=0.75

        self.thumbnailList.setIconSize(QSize(new_size,new_size))
        #self.thumbnailList.setStyleSheet("QListView::item {height: %s;}"%(new_size+6))

    # When selected of folder in the outliner
    def onClickItem(self,item):
        self.thumbnailList.clear()
        #a= TreeWidget(item.text(1))
        #self.middle.addWidget(ThumbnailPanel.createWidget(item.text(1)))
        folder = item.text(1)

        for root, dirs, files in os.walk(folder) :
            for filename in files :
                if os.path.splitext(filename)[1] in ['.png','.jpg'] :
                    full_path = os.path.abspath(os.path.join(root, filename))

                    name = os.path.splitext(filename)[0].split('_')[0].replace('-',' ').capitalize()
                    item = QListWidgetItem(name)
                    item.setIcon(QIcon(full_path))
                    item.full_path = full_path

                    self.thumbnailList.addItem(item)

    # display information when clicking on a thumbnail
    def onClickThumb(self,item) :
        clear_layout(self.rightLayout)

        base_name = os.path.basename((item.full_path))
        dir_name = os.path.dirname((item.full_path))

        description_name = base_name.replace(base_name.split('_')[-1],'description.txt')
        description_path = os.path.join(dir_name,description_name)

        infile =  open(description_path).read()

        self.textPanel = QFrame()
        self.textPanel.setStyleSheet("border : none; background-color : rgb(100,100,100)")

        #self.text

        self.textLayout = QVBoxLayout()
        self.textPanel.setLayout(self.textLayout)
        #Fill layout
        #Text description
        self.textWidget = QPlainTextEdit()
        self.textWidget.setPlainText(infile)
        self.textLayout.addWidget(self.textWidget)
        #Preview Image
        self.previewImage = QLabel()
        self.previewImage.setStyleSheet("border : none;")
        #sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        #sizePolicy.setHeightForWidth(True)
        self.previewImage.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.previewImage.setMinimumSize(256,256)
        self.previewImage.setMaximumSize(256,256)
        self.previewImage.setScaledContents(True)
        #self.previewImage.setWidgetResizable(True)

        thumb = QPixmap(item.full_path)
        self.previewImage.setPixmap(thumb)


        self.rightLayout.addWidget(self.previewImage)
        self.rightLayout.addWidget(self.textPanel)


    def apply_pose(self,item) :
        ob = self.context.scene.objects.active

        clear_layout(self.toolBoxLayout)

        self.frame_current = bpy.context.scene.frame_current

        self.blend = QSlider()
        self.blend.setOrientation(Qt.Horizontal)
        self.blend.setValue(100)
        self.blend.setMaximum(100)

        self.action_left = CheckBox('Left')
        self.action_left.setChecked(True)

        self.action_right = CheckBox('Right')
        self.action_right.setChecked(True)

        self.selected_only = CheckBox('Selected only')
        self.selected_only.setChecked(True)

        self.mirror_pose = CheckBox('Mirror')
        self.mirror_pose.setChecked(False)

        self.toolBoxLayout.addWidget(self.blend)

        row_L_R = QHBoxLayout()
        row_L_R.addWidget(self.action_right)
        row_L_R.addWidget(self.action_left)

        self.toolBoxLayout.addLayout(row_L_R)

        self.toolBoxLayout.addWidget(self.selected_only)
        self.toolBoxLayout.addWidget(self.mirror_pose)

        self.action = {}
        item_basename = os.path.splitext(item.full_path)[0]
        action_txt = item_basename.replace('_thumbnail','_action')+'.txt'
        self.blend.setValue(100)

        with open(action_txt) as poseLib:
            for line in poseLib:
                fcurve = line.split("=")[0]
                value = eval(line.split("=")[1].replace("\n",""))

                self.action[fcurve] = value

        if ob :
            for fcurve,value in self.action.items():
                for path,channel in value.items() :

                    #print(channel.items())
                    for array_index,attributes in channel.items() :
                        correct_path = find_fcurve_path(ob,fcurve,path, array_index)
                        dstChannel = correct_path[0]

                        for index,keypose in enumerate(self.action[fcurve][path][array_index]) :
                            #print(keypose)
                            self.action[fcurve][path][array_index][index][1].append(dstChannel)
                            #if find_mirror(fcurve) :



        self.blend.valueChanged.connect(lambda : self.refresh_pose(action_txt))
        self.action_left.stateChanged.connect(lambda :self.refresh_pose(action_txt))
        self.action_right.stateChanged.connect(lambda :self.refresh_pose(action_txt))
        self.selected_only.stateChanged.connect(lambda : self.refresh_pose(action_txt))
        self.mirror_pose.stateChanged.connect(lambda : self.refresh_pose(action_txt))

        self.refresh_pose(action_txt)

    # Apply the pose or anim to the rig
    def refresh_pose(self,action) :
        ob = self.context.scene.objects.active
        if ob.type=='ARMATURE' and ob.mode == 'POSE' :
            read_anim(self.action,self.blend.value()*0.01,self.action_left.isChecked(),self.action_right.isChecked(),self.selected_only.isChecked(),self.mirror_pose.isChecked(),self.frame_current)

    # When taping in the search bar
    def filterThumbnail(self) :
        items = (self.thumbnailList.item(i) for i in range(self.thumbnailList.count()))


        for w in items :
            if self.search_bar.text().lower() not in w.text().lower() :
                w.setHidden(True)
            else :
                w.setHidden(False)


    def closeEvent(self, event):
        self.widget_close = True
        self.deleteLater()


        #self.setGeometry(300, 300, 300, 200)
