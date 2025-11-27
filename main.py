import sys
import subprocess
import time
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import datetime
 
from root import Ui_MainWindow
 

def checkDirBack(currentPath):
    newDir = os.path.abspath(currentPath)
    newDir = newDir.split('/')
    newDir = newDir[:-1]
    newDir = '/'.join(newDir)

    return newDir if os.path.isdir(newDir) else False

def checkNewPath(path):
    newDir = os.path.abspath(path)
    return newDir if os.path.isdir(newDir) else False


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        header = self.fileTableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.backButton.clicked.connect(lambda: self.backButtonClick())
        self.backButton.setShortcut(QKeySequence("Backspace")) 

        self.inButton.clicked.connect(lambda: self.inButtonClick())


        self.rootsysButton.clicked.connect(lambda: self.rootSysButtonClick())

        self.fileTableWidget.itemDoubleClicked.connect(self.doubleClickItemEvent)

        self.fileTableWidget.itemClicked.connect(self.oneClickItemEvent)

        self.fileTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTableWidget.customContextMenuRequested.connect(self.show_context_menu)

        self.pathLineEdit.textChanged.connect(lambda: self.pathLineEditChanged())


        self.pathLineEdit.setText((os.path.abspath('.')))

    def show_context_menu(self, pos: QPoint):
        item = self.fileTableWidget.itemAt(pos)
        
        if item:
            menu = QMenu(self)

            edit_action = QAction("Rename", self)
            edit_action.triggered.connect(lambda: self.edit_item(item))
            menu.addAction(edit_action)

            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)

            copy_action = QAction("Copy", self)
            copy_action.triggered.connect(lambda: self.copy_item(item))
            menu.addAction(copy_action)

            cut_action = QAction("Cut", self)
            cut_action.triggered.connect(lambda: self.cut_item(item))
            menu.addAction(cut_action)

            menu.exec_(self.fileTableWidget.mapToGlobal(pos))

    def edit_item(self, item: QListWidgetItem):
        os.rename(str(self.old_filename).replace("🗀", ""), item.text())

            
    def delete_item(self, item: QListWidgetItem):
        os.remove(str(self.old_filename).replace("🗀", ""))
        self.showFiles('.')

    def copy_item(self, item: QListWidgetItem):
        pass

    def cut_item(self, item: QListWidgetItem):
        pass
            
    def showFiles(self, dirpath):
        self.clearFileRows()

        currentFiles = os.listdir(dirpath)

        self.pathLineEdit.setText(str(os.path.abspath('.')))

        for file in currentFiles:
            rowPosition = self.fileTableWidget.rowCount()
            self.fileTableWidget.insertRow(rowPosition)
            
            if os.path.isdir(os.path.abspath(file)):
                self.fileTableWidget.setItem(rowPosition , 0, QTableWidgetItem(str("🗀" + file)))
            else:
                self.fileTableWidget.setItem(rowPosition , 0, QTableWidgetItem(str(file)))

            size = os.path.getsize(os.path.abspath(file)) / 1000
            size = str(size) + ' kB'
            self.fileTableWidget.setItem(rowPosition , 1, QTableWidgetItem(str(size)))

            timeCreated = time.ctime(os.path.getctime(file))
            timeCreated = datetime.datetime.strptime(timeCreated, "%a %b %d %H:%M:%S %Y")
            self.fileTableWidget.setItem(rowPosition , 2, QTableWidgetItem(str(timeCreated)))

            timeModify = time.ctime(os.path.getmtime(file))
            timeModify = datetime.datetime.strptime(timeModify, "%a %b %d %H:%M:%S %Y")
            self.fileTableWidget.setItem(rowPosition , 3, QTableWidgetItem(str(timeModify)))

        
    def doubleClickItemEvent(self, item):
        item = self.fileTableWidget.item(item.row(), 0)

        absolutFilePath = os.path.abspath(item.text().replace("🗀", ""))

        if os.path.isdir(absolutFilePath.replace('🗀','')):
            os.chdir(absolutFilePath.replace('🗀',''))
            self.clearFileRows()
            self.pathLineEdit.setText(absolutFilePath.replace('🗀',''))

    def oneClickItemEvent(self, item):
        self.old_filename = item.text()
    
    def backButtonClick(self):

        pathBack = checkDirBack('.')
        if checkDirBack(pathBack):
            self.clearFileRows()
            self.previousDirPath = os.path.abspath('.')
            os.chdir(pathBack)
            self.pathLineEdit.setText(pathBack)

    def inButtonClick(self):
        self.clearFileRows()
        os.chdir(self.previousDirPath)
        self.pathLineEdit.setText(self.previousDirPath)

    def rootSysButtonClick(self):
        self.clearFileRows()
        os.chdir('/')
        self.showFiles('/')

    def clearFileRows(self):
        self.fileTableWidget.setRowCount(0)

    def pathLineEditChanged(self):
        newPath = checkNewPath(self.pathLineEdit.text()) 

        if newPath:
            self.clearFileRows()
            os.chdir(newPath)
            self.showFiles(newPath)


 
app = QtWidgets.QApplication(sys.argv)

qss_file = QFile("Qstyles/MaterialDark.qss")
if qss_file.open(QFile.ReadOnly | QFile.Text):
    stream = QTextStream(qss_file)
    stylesheet = stream.readAll()
    app.setStyleSheet(stylesheet)
    qss_file.close()
else:
    print("Error: Could not open style.qss")

window = MainWindow()
window.show()
app.exec()