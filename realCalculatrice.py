# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:25:27 2019

@author: ykhima
"""

import sys
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

def main() :
    app = QtWidgets.QApplication(sys.argv)
    
    L  = 600
    H = 600
    window = QtWidgets.QWidget()
    window.resize(L, H)
    window.setWindowTitle("Programe Calculatoire")
    
    screen = QtWidgets.QLabel("0", window)
    screen.move(2 + (L/4)*2, (H/5)*0)
    screen.resize((L/4)-3, (H/5)-2)
    
    currentValue = 0
    currentValueInit = True
    currentValueDecimal = 0
    oldValue = 0
    currentOperation = 0
    
    def createButton(x, y, texte, callBack) :
        
        
        button = QtWidgets.QPushButton(texte, window)
        button.move(2 + (L/4)*x, (H/5)*y)
        button.resize((L/4)-3, (H/5)-2)
        button.clicked.connect(callBack)

        return button
        
    def setCurrentValue(v) :
        nonlocal currentValue
        currentValue = v
        screen.setText(format(v, "G"))
        

    
    def delete() :
        nonlocal currentValue, currentValueInit, oldValue
        currentValue = 0
        currentValueInit = True
        oldValue = 0
        
    def relatif() :
        nonlocal currentValue
        currentValue = -currentValue
        

    def operation(n) : 
        def realOperation() :
            nonlocal oldValue, currentValue, currentValueInit, currentOperation
            
            if n == 0 and currentOperation == 1 :
                    setCurrentValue(oldValue + currentValue)
                    
            elif n == 0 and currentOperation == 2 :
                    setCurrentValue(oldValue - currentValue)
                    
            elif n == 0 and currentOperation == 3 :
                    setCurrentValue(oldValue * currentValue)
                    
            elif n == 0 and currentOperation == 4 :
                    setCurrentValue(oldValue / currentValue)
               
            else :
                oldValue = currentValue 
                currentValueInit = True
                currentOperation = n
            
        return realOperation

    def digit(n) :
        def realDigit() :
            
            nonlocal currentValue, currentValueInit, currentValueDecimal 
            
            
            if currentValueInit :
                currentValue = n
            elif currentValueDecimal > 0 :
                currentValue = currentValue + n * 10 ** -currentValueDecimal
                currentValueDecimal = currentValueDecimal + 1
            else :
                currentValue = currentValue * 10 + n
            currentValueInit = False    
            setCurrentValue(currentValue)
            print(currentValue)
            
        return realDigit

    def keyDecimal() :
        nonlocal currentValueDecimal, currentValueInit
        if currentValueDecimal == 0 :
            currentValueDecimal = 1
            currentValueInit = False

    
    createButton(0, 0, "delete", delete)
    createButton(3, 0, "="  ,    operation(0))
    
    createButton(0, 1, "7",      digit(7))
    createButton(1, 1, "8",      digit(8))
    createButton(2, 1, "9",      digit(9))
    createButton(3, 1, "+",      operation(1))
    
    createButton(0, 2, "4",      digit(4))
    createButton(1, 2, "5",      digit(5))
    createButton(2, 2, "6",      digit(6))
    createButton(3, 2, "-",      operation(2))
    
    createButton(0, 3, "1",      digit(1))
    createButton(1, 3, "2",      digit(2))
    createButton(2, 3, "3",      digit(3))
    createButton(3, 3, "*",      operation(3))
    
    createButton(0, 4, ",",      keyDecimal)
    createButton(1, 4, "0",      digit(0))
    createButton(2, 4, "+/-",    relatif)
    createButton(3, 4, "/",      operation(4))
    


    window.show()
    sys.exit(app.exec_())

main()