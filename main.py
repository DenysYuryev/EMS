# pyrcc5 icons.qrc -o icons_rc.py
# pyrcc5 images.qrc -o images_rc.py
# pyuic5 ems_main.ui -o ems_main_ui.py

import os
import sys
import csv
import pandas as pd

from ems_main_ui import *
from ems_calendar_ui import *

from PySide6.QtGui import QPainter, QColor, QColorSpace
from PySide6.QtCharts import QChart

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPalette, QTextCharFormat
from PyQt5.QtCore import Qt

# style sets buttons
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
            effect.setColor(QtGui.QColor(0, 50, 120, 160))
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

        # navigate on stack
        self.ui.stackedWidget.setCurrentWidget(self.ui.stack_1)

        # call calendar
        self.ui.pushButton_calendar.clicked.connect(lambda: self.openCalendar())

        self.ui.pushButton_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_1))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_2))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_3))
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_4))
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_5))
        #
        self.ui.pushButton_11.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_6))
        self.ui.pushButton_11.clicked.connect(lambda checked, dbName='dbIdc': self.sql_con(dbName, 0))
        #self.sql_con(dbName='dbIdc')
        self.ui.pushButton_12.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_7))
        self.ui.pushButton_13.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_8))
        self.ui.pushButton_14.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_9))
        self.ui.pushButton_15.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_10))
        self.ui.pushButton_16.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.stack_11))
        self.ui.pushButton_16.clicked.connect(lambda checked, dbName='dbIdc': self.sql_con(dbName, 0))

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

# SQL connection and data reading
    SERVER_NAME = "VM-SV101-TULCHI\\PLANTIT"
    DATABASE_NAME = "dbIdc"
    USERNAME = "sa"
    PASSWORD = "ProAdmin777"

 # SQL connection
    def sql_con(self, dbName, mva):
        connection = f'DRIVER={{SQL Server}};' \
                     f'SERVER={self.SERVER_NAME};' \
                     f'UID={self.USERNAME};' \
                     f'PWD={self.PASSWORD};' \
                     f'DATABASE={dbName}'
        print(f"{connection}")
        global db
        try:
            db = QSqlDatabase.addDatabase('QODBC')
            db.setDatabaseName(connection)
            self.ui.plainTextEdit.appendPlainText(f'Processing connection to... : {self.SERVER_NAME}')

            if db.open():
                print('Connection to SQL server successfully')
                self.ui.plainTextEdit.appendPlainText('Connection to SQL server successfully')

                currentWidget = self.ui.stackedWidget.currentWidget()
                if currentWidget == self.ui.stack_6 and mva == 0:
                    self.disp_data('tblEmsPowerMeter', 6)
                elif currentWidget == self.ui.stack_11 and mva == 0:
                    self.disp_data('tblEmsObject', 11)
            else:
                self.ui.plainTextEdit.appendPlainText('Connection to SQL server failed')
                print('Connection to SQL server failed')
                return
        except Exception as Error:
            res = QtWidgets.QMessageBox.critical(self, 'Error', f"Read data from SQL error: {Error}.\n")
            if res == QtWidgets.QMessageBox.Ok:
                db.close()
                return

    def disp_data(self, table_name, stack_num):

        print(f"Table name: {table_name} \n Stack num: {stack_num}")

        SQL_STATEMENT = f'SELECT * FROM dbo.{table_name}'
        self.ui.plainTextEdit.appendPlainText(f'Processing query... : {SQL_STATEMENT}')
        try:
            qry = QSqlQuery(db)
            qry.prepare(SQL_STATEMENT)
            qry.exec()

            fields = qry.record().count()
            rows = qry.numRowsAffected()

            print(f'Fields: {fields} \n Rows: {rows}')
            self.ui.plainTextEdit.appendPlainText(f'Fields: {fields} \n Rows: {rows}')


            if stack_num == 6:
                tbl = self.ui.table_power_cnt
                self.ui.table_power_cnt.setColumnCount(fields)
            elif stack_num == 11:
                tbl = self.ui.table_product_cnt
                self.ui.table_product_cnt.setColumnCount(fields)

            print(f"Table: {tbl}")

            list_fields = []
            list_fields.clear()
            if fields > 0:
                for field in range(fields):
                    item = qry.record().fieldName(field)
                    list_fields.append(item)
                    tbl.setColumnWidth(field, len(list_fields[field]))
                print(f'Item fields: {list_fields}')
                tbl.setHorizontalHeaderLabels(list_fields)
                tbl.resizeColumnsToContents()

            item = []
            if rows > 0:
                qry.first()
                for r in range(rows):
                    row = tbl.rowCount()
                    tbl.setRowCount(r + 1)
                    item.clear()
                    for c in range(fields):
                        item.append(qry.value(c))
                        tbl.setItem(row, c, QtWidgets.QTableWidgetItem(str(item[c])))
                    qry.next()
                    print(f'Item {row}: {item}')
                tbl.resizeColumnsToContents()
            db.close()
            return
        except Exception as Error:
            res = QtWidgets.QMessageBox.critical(self, f'Error', f"Read data from SQL error: {Error}.\n")
            if res == QtWidgets.QMessageBox.Ok:
                db.close()
                return


    def read_MVA (self, sDate, eDate, nTag = 'CNT_003-FT01'):

        print(f'Start date to MVA: {sDate}\nEnd Date to MVA: {eDate}')

        if sDate != '' and eDate != '':
            SQL_STATEMENT = f"EXEC dbo.sp_EmsGetMVAData ''{sDate} 00:00:00'', ''{eDate} 23:59:59'', ''{nTag}''"
            print(f"Request to MVA: {SQL_STATEMENT}")

            #self.sql_con('dbIdc', 1)
            print(f"Test")
            try:
                qry = QSqlQuery(db)
                qry.prepare(SQL_STATEMENT)
                qry.exec()

                fields = qry.record().count()
                rows = qry.numRowsAffected()
                print(f"Fields = {fields}\nRows = {rows}")
                return
            except Exception as Error:
                res = QtWidgets.QMessageBox.critical(self, f'Error', f"Read data from MVA error: {Error}.\n")
                if res == QtWidgets.QMessageBox.Ok:
                    db.close()
                    return
        elif sDate != '' and eDate == '':
            SQL_STATEMENT = f"EXEC dbo.sp_EmsGetMVAData '{sDate} 00:00:00', '{sDate} 23:59:59', '{nTag}'"
            print(f"Request to MVA: {SQL_STATEMENT}")
            try:
                qry = QSqlQuery(db)
                qry.prepare(SQL_STATEMENT)
                qry.exec()

                fields = qry.record().count()
                rows = qry.numRowsAffected()

                currentWidget = self.ui.stackedWidget.currentWidget()
                if currentWidget == self.ui.stack_6:
                    stack_num = 6
                elif currentWidget == self.ui.stack_11:
                    stack_num = 11

                if stack_num == 6:
                    tbl = self.ui.table_power_cnt
                    self.ui.table_power_mva.setColumnCount(fields)
                elif stack_num == 11:
                    tbl = self.ui.table_product_cnt
                    self.ui.table_product_mva.setColumnCount(fields)

                list_fields = []
                list_fields.clear()
                if fields > 0:
                    for field in range(fields):
                        item = qry.record().fieldName(field)
                        list_fields.append(item)
                        tbl.setColumnWidth(field, len(list_fields[field]))
                    print(f'Item fields: {list_fields}')
                    tbl.setHorizontalHeaderLabels(list_fields)
                    tbl.resizeColumnsToContents()

                item = []
                if rows > 0:
                    qry.first()
                    for r in range(rows):
                        row = tbl.rowCount()
                        tbl.setRowCount(r + 1)
                        item.clear()
                        for c in range(fields):
                            item.append(qry.value(c))
                            tbl.setItem(row, c, QtWidgets.QTableWidgetItem(str(item[c])))
                        qry.next()
                        print(f'Item {row}: {item}')
                    tbl.resizeColumnsToContents()
                db.close()
                return
            except Exception as Error:
                res = QtWidgets.QMessageBox.critical(self, f'Error', f"Read data from MVA error: {Error}.\n")
                if res == QtWidgets.QMessageBox.Ok:
                    db.close()
                    return

    # Date picker
    def openCalendar(self):
        dialog = Calendar(self)
        dialog.exec_()

# calendar class window
class Calendar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Calendar, self).__init__(parent)
        self.ui = Ui_Calendar()
        self.ui.setupUi(self)

        self.SDate = None
        self.EDate = None


        self.highlighter = QTextCharFormat()
        self.highlighter.setBackground(self.palette().brush(QPalette.Highlight))
        self.highlighter.setForeground(self.palette().color(QPalette.HighlightedText))

        self.ui.calendarWidget.clicked.connect(self.select_date_range)
        self.ui.pushButton_apply.clicked.connect(self.print_dates_selected)

    # present selection dates range or one date
    def print_dates_selected(self):
        if self.SDate and self.EDate:
            self.start_date = min(self.SDate.toPyDate(), self.EDate.toPyDate())
            self.end_date = max(self.SDate.toPyDate(), self.EDate.toPyDate())
            date_list = pd.date_range(start=self.start_date, end=self.end_date)
            print(F"S: {self.start_date}\nE: {self.end_date}")
            print(date_list)
            #self.SDate = start_date
            #self.EDate = end_date
            App.read_MVA(self.start_date, self.end_date, '')
            #print(f'Start date: {self.SDate}\nEnd date: {self.EDate}')
            self.close()
        else:
            #self.SDate = self.SDate.toPyDate()
            App.read_MVA(self.start_date, '', '')
            #print(f'Selection date: {self.SDate}')
            self.close()

    # calendar
    def select_date_range(self, date_value):
        fDate = date_value.toString(QtCore.Qt.ISODate)
        print(f'Data: {fDate}')
        self.highlight_range(QTextCharFormat())

        # keyboard modifiers
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        # log ections
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Ctr+Click')
        elif modifiers == (QtCore.Qt.ControlModifier & modifiers == QtCore.Qt.ShiftModifier):
            print('Ctr+Shift+Click')
        else:
            print('Click')

        # shift + click action to highlight range of dates
        if (modifiers == QtCore.Qt.ShiftModifier) and self.SDate:
            self.EDate = date_value
            self.highlight_range(self.highlighter)
        else:
            self.SDate = date_value
            self.EDate = None

    # highlight range of dates
    def highlight_range(self, format):
        if self.SDate and self.EDate:
            print(f'Date range: {self.SDate.toPyDate()} - {self.EDate.toPyDate()}')
            d1 = min(self.SDate, self.EDate)
            d2 = max(self.SDate, self.EDate)
            while d2 >= d1:
                self.ui.calendarWidget.setDateTextFormat(d1, format)
                d1 = d1.addDays(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec_())
