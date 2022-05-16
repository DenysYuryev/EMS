# pyrcc5 icons.qrc -o icons_rc.py
# pyrcc5 images.qrc -o images_rc.py
# pyuic5 ems_main.ui -o ems_main_ui.py

import os
import sys
import csv

from ems_main_ui import *
from ems_main_ui import Ui_MainWindow

from PySide6.QtGui import QPainter, QColor, QColorSpace
from PySide6.QtCharts import QChart

from random import randrange
from functools import partial

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

shadow_elements = {
    "frame_left_menu",
    "frame_menu",
    "frame_body",
    "frame_footer"
}


# main class window
class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # shadow effect style
        for x in shadow_elements:
            effect = QtWidgets.QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(10)
            effect.setColor(QColor(50, 120, 160))
            effect.setXOffset(0)
            effect.setYOffset(0)
            getattr(self.ui, x).setGraphicsEffect(effect)

        # hide windows tittle bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # set window icon and title
        self.setWindowIcon(QtGui.QIcon("./Images/Logo/Icon_EnMS_Module.png"))
        self.setWindowTitle("EMS")

        # transparent background
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # hide/show menu
        self.ui.pushButton_menu.clicked.connect(self.slideLeftMenu)

        # window fold
        self.ui.pushButton_window_fold.clicked.connect(lambda: self.showMinimized())

        # window minimize/maximize
        self.ui.pushButton_window_resize.clicked.connect(lambda: self.mini_maximize())

        # window close
        self.ui.pushButton_window_close.clicked.connect(lambda: self.close())

        # nevigate on stack
        self.ui.pushButton_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_1))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_2))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_3))
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_4))
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_5))

        # move window on mouse drag event on tittle bar
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.ui.frame_top.mouseMoveEvent = moveWindow

    def mini_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.pushButton_window_resize.setIcon(QtGui.QIcon("./Icons/Drip Icons V2/expand.svg"))
        else:
            self.showMaximized()
            self.ui.pushButton_window_resize.setIcon(QtGui.QIcon("./Icons/Drip Icons V2/contract.svg"))

    # mouse current position
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def slideLeftMenu(self):
        width = self.ui.frame_left_menu.width()
        # if minimized
        if width == 0:
            newWidth = 250
            self.ui.pushButton_menu.setIcon(QtGui.QIcon("./Icons/Drip Icons V2/chevron-left.svg"))
        # if maximized
        else:
            newWidth = 0
            self.ui.pushButton_menu.setIcon(QtGui.QIcon("./Icons/Drip Icons V2/menu.svg"))

        # animate the transition
        self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec_())
