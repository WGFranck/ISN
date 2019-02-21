# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 17:39:46 2019

@author: Samy
"""

import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt



def main() :
    app = QtWidgets.QApplication(sys.argv)
    
    L  = 600
    H = 600
    window = QtWidgets.QWidget()
    window.resize(L, H)
    window.setWindowTitle("Programe de test")
    
    def println():
        print("Print")

    def createButton(x, y, texte, callBack) :
        
        
        button = QtWidgets.QPushButton(texte, window)
        button.move(2 + (L/4)*x, (H/5)*y)
        button.resize((L/4)-3, (H/5)-2)
        button.clicked.connect(callBack)

        return button
    

    
    testButton = QtWidgets.QPushButton("HelloWorld", window)
    testButton.resize(100, 50)
    testButton.move(0, 550)
    menuPasGlobal = QtWidgets.QMenu("afficher Un Truc", window)
    menuGlobal = QtWidgets.QMenu("testLesGens", window)
    menuGlobal.addMenu(menuPasGlobal)
    liste = QtWidgets.QPushButton.setMenu(testButton, menuGlobal)
    
    # autreButton = QtWidgets.QPushButton("HelloWorld", window)
    myToolbar = QtWidgets.QToolBar("test", window)
    # myToolbar.move(300,0)
    # myToolbar.addWidget()
    
    
    
    
    
    window.show()
    sys.exit(app.exec_())

main()