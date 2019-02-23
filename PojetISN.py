"""
@author: ykhima
"""

import sys 
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QLine, QRect

def main() :
    
    L  = 700
    H = 800
#-----------------------------------------------------------
    class windowEvent(QtWidgets.QMainWindow):
#-----------------------------------------------------------
         def __init__(self):
            
            super().__init__()
            self.setMouseTracking(True)            
#-----------------------------------------------------------
         def mouseMoveEvent(self, event):
            
            self.cursorPos = event.pos() 
            self.update()
#-----------------------------------------------------------
         def mousePressEvent(self, event):
            nonlocal L, H
            
            if self.cursorPos.x() > 10 and self.cursorPos.x() < L-20 and self.cursorPos.y() > 10 and self.cursorPos.y() < (H/2)-20:
                print("vous êtes dans la zone de travail")
                
                painter = QPainter(self)
                pen = QtGui.QPen(Qt.red)
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawEllipse(self.cursorPos.x()-5, self.cursorPos.y()-5,10,10)
            else :
                print("vous n'êtes pas dans la zone de travail")
                
#-----------------------------------------------------------
         def paintEvent(self, event):
            nonlocal L, H
            
            painter = QPainter(self)
            brush = QtGui.QBrush(Qt.gray)
            painter.setBrush(brush)
            pen = QtGui.QPen(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(10, 10, L-20, (H/2)-20)
            
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(self.cursorPos.x()-2.5, self.cursorPos.y()-2.5,5,5)
#-----------------------------------------------------------
         def resizeEvent(self, event):
            nonlocal L, H
            
            windowSize = self.size()
            L = windowSize.width()
            H = windowSize.height()
#-----------------------------------------------------------
    def elecMode():
        print("électique Mode")
        
    def logicMode():
        print("Porte logique Mode")
        
    def closeProg():
        mainWindow.close()
        
    def null():
        print("null")
#-----------------------------------------------------------
    def createButton(posX, posY, sizeX, sizeY, texte, widget, callBack) :
        
        button = QtWidgets.QPushButton(texte, widget)
        button.move(posX, posY)
        button.resize(sizeX, sizeY)
        button.clicked.connect(callBack)

        return button
#-----------------------------------------------------------
    app = QtWidgets.QApplication(sys.argv)
    
    size = QtWidgets.QApplication.desktop().screenGeometry()
    screenPosX = size.width()
    screenPosY = size.height()
#-----------------------------------------------------------
    mainWindow = QtWidgets.QMainWindow()
    mainWindow.resize(L, H)
    mainWindow.move((screenPosX/2)-(L/2), (screenPosY/2)-(H/2))
    mainWindow.setCentralWidget(windowEvent())
    mainWindow.setWindowTitle("Programe de test")
#-----------------------------------------------------------  
    interface = QtWidgets.QDockWidget("Guide d'utilisation")
    interface.resize(L, H/2)
    interface.move(0, 0)
#-----------------------------------------------------------
    createButton(10, (H*3/6), L-20, (H/6)-10, "Création de schémat électrique", mainWindow, elecMode)
    createButton(10, (H*4/6), L-20, (H/6)-10, "Création de schémat logique", mainWindow, logicMode)
    createButton(10, (H*5/6), (L/2)-20, (H/6)-10, "Besoin d'aide ?", mainWindow, null)
    createButton((L/2)+10, (H*5/6), (L/2)-20, (H/6)-10, "Close", mainWindow, closeProg)
#-----------------------------------------------------------   
    mainWindow.show()
    sys.exit(app.exec_())
#-----------------------------------------------------------   
main()