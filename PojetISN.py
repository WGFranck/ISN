"""
@author: ykhima
"""
#A faire :

#-peut être une QDockWindow pour demander la taille de la fenêtre et le coefElement avant de lancer main() 
#vue que l'interface est en fonction de L et H

#un pushbutton pour mettre du texte pour les unitée et les valeurs

#utiliser un QDockWidget pour le texte de "besoin d'aide"

#un mode QCM ?

#créer peut être à la fin un mode save-load

import sys, math
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QLine, QRect, QPoint


def main() :

#Taille de la fenètre MODIFIABLE dans le programme
#-et modifiable un jour par l'utilisateur 
#-toute taille disponible tant que c'est suppérieur 250 et pair
    L  = 700
    H = 800
    
#Booléan du boutton de la souris pour la position des éléments.
    clickCanvas = False
    
#l'utilisateur doit clicker une prmière fois pour appeler un élément puis un second click pour le placer sur le canevas
    initClick = False
    
    rightClickCanvas = False
#initialisation des positions
    cursorPos = QPoint()
    clickPos = QPoint()
    startLinePos = QPoint()
#Taille des éléments MODIFIABLE dans le programme
#-et modifiable un jour par l'utilisateur 
#-coefElement >= 2 et coefElement pair et c'est lisible quand c'est >=6
    coefElement = 10
    
#élement choisit par l'utilisateur    
    userElement = 0
    userRotation = 0
    
    intWindowMode = 0
    
    linearMode = False
    lineMode = False
    
#taille du canevas en fonction de la taille de l'écran non modifiable par l'utilisateur 
#-valeur pour intWindowMode = 0 servira pour afficher une image
    canvas = QRect(10, 10, L-20, (H*7/9)-20)
    
#Canvas Example est le canvas qui permet de changer d'element (théoriquement)    
    canvasExample = QRect((L/2)-50, (H*8/9)-50, L/7, H/7) 
  
#initialisation des Button du Home Menu et du mode de création avec un tableau
    homeButton = {}
    editorButton = {}

    elementOnCanvas = {}
    elementOnCanvas[0] = 0
    
    elementOnCanvasPos = {}
    elementOnCanvasPos[0] = 0
    
    elementOnCanvasRotation = {}
    elementOnCanvasRotation[0] = 0
    
    lineOnCanvas = {}
    lineOnCanvas[0] = 0
#-----------------------------------------------------------     
#-----------------------------------------------------------     
#class des différents évenement de mainWindow
    class windowEvent(QtWidgets.QMainWindow):
#-----------------------------------------------------------
         def __init__(self):
            super().__init__()
            self.setMouseTracking(True)
            self.setFocusPolicy(True)
#-----------------------------------------------------------
         def mouseMoveEvent(self, event):
            nonlocal cursorPos
            cursorPos = event.pos()
            self.update()

#-----------------------------------------------------------            
         def mousePressEvent(self, event):
            nonlocal clickCanvas, initClick, cursorPos, clickPos, userElement, intWindowMode
            nonlocal userRotation, startLinePos, lineMode, rightClickCanvas
            
            if event.button() == Qt.RightButton and canvas.contains(canvas) and not intWindowMode == 0:
                rightClickCanvas = True
                clickCanvas = False
                
                if not lineMode:
                    initClick = True
                
            if initClick:
                clickPos = cursorPos
                if lineMode:    
                    startLinePos = clickPos
            
            if not intWindowMode == 0 and canvasExample.contains(cursorPos) and not lineMode:
                clickCanvas = False
                userElement = userElement + 1
                initClick = False
                
                if userElement == len(dictElementElec) and intWindowMode == 1 or userElement == len(dictElementLogic) and intWindowMode == 2:
                    userElement = 0
                
            elif not intWindowMode == 0 and canvas.contains(cursorPos) and not canvasExample.contains(clickPos):
               clickCanvas = True
               initClick = not initClick
               
            elif not intWindowMode == 0 and (not canvas.contains(cursorPos) or canvasExample.contains(cursorPos)):
                print("vous n'êtes pas dans la zone de travail")
                clickCanvas = False
                initClick = False
                
            self.update()
#-----------------------------------------------------------
         def paintEvent(self, event):
            nonlocal clickCanvas, initClick, clickPos, cursorPos, startLinePos, userRotation, rightClickCanvas
            nonlocal canvas, dictElementElec, canvasExample, lineMode, linearMode
            nonlocal elementOnCanvas, elementOnCanvasPos, elementOnCanvasRotation, lineOnCanvas
            
            #initialisation du QPainter
            painter = QPainter(self)
            brush = QtGui.QBrush(Qt.lightGray)
            pen = QtGui.QPen(Qt.black)
            pen.setWidth(2)
            painter.setPen(pen)
            
            #dessin du canvas
            if not intWindowMode == 0 :
                painter.setBrush(brush)
                painter.drawRect(canvas)
                painter.drawRect(canvasExample)    
                painter.setBrush(Qt.NoBrush)
            
                temp = clickPos
                
                clickPos = canvasExample.center()
                
                if intWindowMode == 1:
                    dictElementElec[userElement](painter)
                elif intWindowMode == 2:
                    dictElementLogic[userElement](painter)
                    
                clickPos = temp
                
            if initClick:
                clickPos = cursorPos

            if clickCanvas and not intWindowMode == 0 and canvas.contains(clickPos) and not canvasExample.contains(cursorPos) and not lineMode :
                
                if intWindowMode == 1:
                    dictElementElec[userElement](painter)
                elif intWindowMode == 2:
                    dictElementLogic[userElement](painter)
                
                if not initClick and not rightClickCanvas:
                    
                    if elementOnCanvasPos[0] == 0:
                        elementOnCanvas[0] = userElement
                        elementOnCanvasPos[0] = clickPos
                        elementOnCanvasRotation[0] = userRotation
                        clickCanvas = False
                    
                    else :
                        elementOnCanvas[len(elementOnCanvas)] = userElement
                        elementOnCanvasPos[len(elementOnCanvasPos)] = clickPos
                        elementOnCanvasRotation[len(elementOnCanvasRotation)] = userRotation
                        clickCanvas = False
                        
                elif rightClickCanvas:
                    clickCanvas = False
                    rightClickCanvas = False
                    
            if not elementOnCanvasPos[0] == 0  :
                
                for n in range(len(elementOnCanvas)):
                    temp = userRotation
                    temp2 = clickPos
                    
                    
                    clickPos = elementOnCanvasPos[n]
                    userRotation = elementOnCanvasRotation[n]
                    if intWindowMode == 1:
                        dictElementElec[elementOnCanvas[n]](painter)
                    elif intWindowMode == 2:
                        dictElementLogic[elementOnCanvas[n]](painter)
                    
                    userRotation= temp
                    clickPos = temp2
                
            if not lineOnCanvas[0] == 0:
                for n in range(len(lineOnCanvas)):
                    painter.drawLine(lineOnCanvas[n])
            
            
            if lineMode and clickCanvas and canvas.contains(clickPos) and not intWindowMode == 0 :
                
                if linearMode:
                    
                    temp = cursorPos-startLinePos
                    temp1 = temp.x()
                    temp2 = temp.y()
                
                    if abs(temp1) <= abs(temp2):
                        cursorPos.setX(startLinePos.x())

                    elif abs(temp2) <= abs(temp1) :
                        cursorPos.setY(startLinePos.y())
                    
                painter.drawLine(startLinePos.x(), startLinePos.y(), cursorPos.x(), cursorPos.y())
                
                if initClick and not rightClickCanvas:
                    if lineOnCanvas[0] == 0:
                        lineOnCanvas[0] = QLine(startLinePos.x(), startLinePos.y(), cursorPos.x(), cursorPos.y())
                        clickCanvas = True
                        initClick = False
                        startLinePos = cursorPos

                    else :
                        lineOnCanvas[len(lineOnCanvas)] = QLine(startLinePos.x(), startLinePos.y(), cursorPos.x(), cursorPos.y())
                        clickCanvas = True
                        initClick = False
                        startLinePos = cursorPos

                elif rightClickCanvas:
                    clickCanvas = False
                    initClick = True
                    rightClickCanvas = False
                    startLinePos = cursorPos
                    
            self.update()
#-----------------------------------------------------------
#-----------------------------------------------------------   
#Les class des éléments a pour but de dessiner les éléments en fonction d'un repère
    class elementElec(QPainter):        
#-----------------------------------------------------------     
        def resistance(self):
            #base
            self.drawLine(createLine(-1, -2, 1, -2))
            self.drawLine(createLine(1, -2, 1, 2))
            self.drawLine(createLine(1, 2, -1, 2))
            self.drawLine(createLine(-1, 2, -1, -2))
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
#-----------------------------------------------------------
        def generator(self):
            #base
            self.drawEllipse(createEllipse(0, 0, 4, 4))
            #cables
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
            #"+"
            self.drawLine(createLine(-2, -3, -2, -2))
            self.drawLine(createLine(-2.5, -2.5, -1.5, -2.5))
            #"-"
            self.drawLine(createLine(-2.5, 2.5, -1.5, 2.5))
#-----------------------------------------------------------
        def ground(self):
            #base
            self.drawLine(createLine(-2, -0.5, +2, -0.5))
            self.drawLine(createLine(-1.5, 0, 1.5, 0))
            self.drawLine(createLine(-1, 0.5, 1, 0.5))
            #cable
            self.drawLine(createLine(0, -0.5, 0, -2))
#----------------------------------------------------------
        def diode(self):
            #triangle
            self.drawLine(createLine(-1.5, 1.5, 1.5, 1.5))
            self.drawLine(createLine(1.5, 1.5, 0,-1.5))
            self.drawLine(createLine(0, -1.5, -1.5, 1.5))
            #trait de la katode
            self.drawLine(createLine(-1.5, -1.5, 1.5, -1.5))
            #cables
            self.drawLine(createLine(0, -2.5, 0, 2.5))
            
        def diodeZener(self):
            elementElec.diode(self)
            self.drawLine(createLine(1.5, -1.5, 1.5, -1))
#-----------------------------------------------------------
        def transistor(self):
            #base
            self.drawLine(createLine(-2, -2, -2, 2))
            self.drawLine(createLine(-2, -1, 0, -2))
            self.drawLine(createLine(-2, 1, 0, 2))
            #cable
            self.drawLine(createLine(-2, 0, -4, 0))
            self.drawLine(createLine(0, -2, 0, -4))
            self.drawLine(createLine(0, 2, 0, 4))
#-----------------------------------------------------------
        def coil(self):
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
            #base 
            for n in range(0,4):
                self.drawArc(createEllipse(0, -1.5 + n, 1, 1), createHalfAngle(math.pi*3/2), createHalfAngle(0))
#-----------------------------------------------------------
        def capacitor(self):
            #base
            self.drawLine(createLine(-1.5, -0.5, 1.5, -0.5))
            self.drawLine(createLine(-1.5, 0.5, 1.5, 0.5))
            #cable
            self.drawLine(createLine(0, -0.5, 0, -2.5))
            self.drawLine(createLine(0, 0.5, 0, 2.5))
#-----------------------------------------------------------
        def AOP(self):
            #triangle
            self.drawLine(createLine(-3, 3, 3, 3))
            self.drawLine(createLine(3, 3, 0,-3))
            self.drawLine(createLine(0, -3, -3, 3))
            #"+"
            self.drawLine(createLine(-2, 3, -2, 4))
            self.drawLine(createLine(-2.5, 3.5, -1.5, 3.5))
            #"-"
            self.drawLine(createLine(1.5, 3.5, 2.5, 3.5))
            #cable
            self.drawLine(createLine(0, -3, 0, -5))
            self.drawLine(createLine(-1, 3, -1, 5))
            self.drawLine(createLine(1, 3, 1, 5))
            
        def arrowVoltage(self):
            self.drawLine(createLine(0, -3, 0, 3))
            self.drawLine(createLine(-0.5, -2.5, 0, -3))
            self.drawLine(createLine(0, -3, 0.5, -2.5))
            
        def arrowCurrent(self):
            self.drawLine(createLine(-0.5, 0, 0, -1))
            self.drawLine(createLine(0, -1, 0.5, 0))
#----------------------------------------------------------     
#----------------------------------------------------------     
#"dicitonaire" faisant l'office d'un "Switch Case" et regroupe toutes les fonctions de la class element dans un tableau, il ne reste plus qu'à faire dictElementElec[int](painter)
    dictElementElec = {
           0 : elementElec.resistance,
           1 : elementElec.generator,
           2 : elementElec.ground,
           3 : elementElec.diode,
           4 : elementElec.diodeZener,
           5 : elementElec.transistor,
           6 : elementElec.coil,
           7 : elementElec.capacitor,
           8 : elementElec.AOP,
           9 : elementElec.arrowVoltage,
           10 : elementElec.arrowCurrent, }
#-----------------------------------------------------------     
#-----------------------------------------------------------
#-----------------------------------------------------------     
    class elementLogic(QPainter):  
        
        def bufferGate(self):
            #triangle
            self.drawLine(createLine(-2, 2, 2, 2))
            self.drawLine(createLine(2, 2, 0,-2))
            self.drawLine(createLine(0, -2, -2, 2))
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
            
        def notGate(self):
            elementLogic.bufferGate(self)
            self.drawEllipse(createEllipse(0, -2, 1, 1))
            
        def orGate(self):
            #cable
            self.drawLine(createLine(0, -2, 0, -4))
            self.drawLine(createLine(-1, 1.5, -1, 4))
            self.drawLine(createLine(1, 1.5, 1, 4))
            #base
            self.drawArc(createEllipse(0, 2, 4, 8), createHalfAngle(math.pi*2), createHalfAngle(0))
            self.drawArc(createEllipse(0, 2.5, 4, 2), createHalfAngle(math.pi*2), createHalfAngle(0))
            
        def norGate(self):
            elementLogic.orGate(self)
            self.drawEllipse(createEllipse(0, -2.5, 1, 1))
        
        def xorGate(self):
            elementLogic.orGate(self)
            self.drawArc(createEllipse(0, 3, 4, 1), createHalfAngle(math.pi*22), createHalfAngle(0))
            
        def nxorGate(self):
            elementLogic.norGate(self)
            elementLogic.xorGate(self)
            
            
        def andGate(self):
            #cable
            self.drawLine(createLine(-1, 2, -1, 4))
            self.drawLine(createLine(1, 2, 1, 4))
            self.drawLine(createLine(0, -1, 0, -4))
            #base
            self.drawArc(createEllipse(0, 0, 4, 2), createHalfAngle(math.pi*2), createHalfAngle(0))
            self.drawLine(createLine(-2, 0, -2, 2))
            self.drawLine(createLine(-2, 2, 2, 2))
            self.drawLine(createLine(2, 2, 2, 0))
            
        def nandGate(self):
            elementLogic.andGate(self)
            self.drawEllipse(createEllipse(0, -1.5, 1, 1))
#-----------------------------------------------------------     
#-----------------------------------------------------------
#-----------------------------------------------------------   
    dictElementLogic = {
           0 : elementLogic.bufferGate,
           1 : elementLogic.notGate,
           2 : elementLogic.andGate,
           3 : elementLogic.nandGate,
           4 : elementLogic.orGate,
           5 : elementLogic.norGate,
           6 : elementLogic.xorGate,
           7 : elementLogic.nxorGate,
           }
    
#Les fonctions suivantes ont pour but de créer les éléments en fonction du coef et de la souris (repère : clickPos, coefElement* x->, coefElement* y->)
    def createPointX(X):
        nonlocal clickPos, coefElement
        return clickPos.x()+X*coefElement
  
    def createPointY(Y):
        nonlocal clickPos, coefElement
        return clickPos.y()+Y*coefElement
  
    def createLine(x1, y1, x2, y2):
        nonlocal clickPos, coefElement, userRotation
        
        newX1 = clickPos.x() + x1*math.cos(userRotation)*coefElement - y1*math.sin(userRotation)*coefElement
        newY1 = clickPos.y() + x1*math.sin(userRotation)*coefElement + y1*math.cos(userRotation)*coefElement
        newX2 = clickPos.x() + x2*math.cos(userRotation)*coefElement - y2*math.sin(userRotation)*coefElement
        newY2 = clickPos.y() + x2*math.sin(userRotation)*coefElement + y2*math.cos(userRotation)*coefElement
        
        return QLine(newX1, newY1, newX2, newY2)
    
    def createHalfAngle(startAngle):
        nonlocal userRotation
        if startAngle == 0:
            return math.degrees(math.pi)*16
        else :
            return math.degrees(startAngle-userRotation)*16
        
    def createEllipse(x, y, largeur, hauteur): #faut faire la rotation sur le cercle en lui même donc la c'est faux
        nonlocal clickPos, coefElement, userRotation
        
        newX1 = clickPos.x() + (x-largeur/2)*math.cos(userRotation)*coefElement - (y-hauteur/2)*math.sin(userRotation)*coefElement
        newY1 = clickPos.y() + (x-largeur/2)*math.sin(userRotation)*coefElement + (y-hauteur/2)*math.cos(userRotation)*coefElement

        newX2 = largeur*math.cos(userRotation)*coefElement - hauteur*math.sin(userRotation)*coefElement
        newY2 = largeur*math.sin(userRotation)*coefElement + hauteur*math.cos(userRotation)*coefElement

        return QRect(newX1, newY1, newX2, newY2)
#-----------------------------------------------------------           
    def createButton(posX, posY, sizeX, sizeY, texte, widget, callBack) :
        
        button = QtWidgets.QPushButton(texte, widget)
        button.move(posX, posY)
        button.resize(sizeX, sizeY)
        button.clicked.connect(callBack)
        return button
    
#Differents callBacks
    def elecMode():
        windowMode(1)

    def logicMode():
        windowMode(2)
        
    def closeProg():
        mainWindow.close()
        
    def clearAll():
        nonlocal elementOnCanvas, elementOnCanvasPos, elementOnCanvasRotation
        nonlocal userRotation, cursorPos, clickPos, lineOnCanvas, lineMode, initClick
        
        userRotation = 0
        
        elementOnCanvas = {}
        elementOnCanvas[0] = 0
    
        elementOnCanvasPos = {}
        elementOnCanvasPos[0] = 0
    
        elementOnCanvasRotation = {}
        elementOnCanvasRotation[0] = 0
        
        cursorPos = QPoint()
        clickPos = QPoint()
        
        lineOnCanvas = {}
        lineOnCanvas[0] = 0
        
        if lineMode:
            initClick = True
        
    def returnHomeMenu():
        nonlocal userElement, clickCanvas, initClick, lineMode, clickCanvas, userRotation, linearMode
        userElement = 0
        userRotation = 0
        clickCanvas = False
        initClick = False
        lineMode = False
        linearMode = False
        
        clearAll()
        windowMode(0)
        
    def addRotation():
        nonlocal userRotation
        userRotation = userRotation + math.pi/2
        if userRotation == math.pi*2:
            userRotation = 0
        
    def buttonlineMode():
        nonlocal lineMode, initClick, editorButton, clickCanvas

        clickCanvas = False
        if editorButton[0].isChecked():
            lineMode = True
            initClick = True
            
        else :
            lineMode = False
            initClick = False
            
    def changeLinearMode():
        nonlocal linearMode, lineMode, clickCanvas, editorButton, initClick
       
        if editorButton[1].isChecked() :
            linearMode = True            
        else :
            linearMode = False
        
    def null():
        print("null")
        
#cette fonction a pour but de regler les bouttons des deux modes (home et création)
    def windowMode(state):
        nonlocal H, L, mainWindow, canvas, homeButton, editorButton, intWindowMode
        intWindowMode = state 
        
        if state == 0 :
            mainWindow.close()
            for n in range(len(editorButton)):
                editorButton[n].close()

            homeButton[0] = createButton(10, (H*3/6), L-20, (H/6)-10, "Création de schémas électriques", mainWindow, elecMode)
            homeButton[1] = createButton(10, (H*4/6), L-20, (H/6)-10, "Création de schémas logiques", mainWindow, logicMode)
            homeButton[2] = createButton(10, (H*5/6), (L/2)-20, (H/6)-10, "Besoin d'aide ?", mainWindow, null)
            homeButton[3] = createButton((L/2)+10, (H*5/6), (L/2)-20, (H/6)-10, "Fermer l'application", mainWindow, closeProg)
        else :
            mainWindow.close()
            for n in range(len(homeButton)) :
                homeButton[n].close()

            editorButton[0] = createButton(10, (H*7/9), (L/4)-20, (H/8)-20, "Cable", mainWindow, buttonlineMode)
            editorButton[0].setCheckable(True)
            editorButton[1] = createButton((L*3/12), (H*7/9), (L/8)-20, (H/8)-20, "lineHor/Vert", mainWindow, changeLinearMode)
            editorButton[1].setCheckable(True)
            editorButton[2] = createButton(10, (H*8/9), (L/4)-20, (H/8)-20, "Tout suppimer", mainWindow, clearAll)
            editorButton[3] = createButton((L*3/4), (H*7/9), (L/4)-20, (H/8)-20, "Retour", mainWindow, returnHomeMenu)    
            editorButton[4] = createButton((L*3/4), (H*8/9), (L/4)-20, (H/8)-20, "Fermer l'application", mainWindow, closeProg)
            editorButton[5] = createButton((L*3/12), (H*8/9), (L/8)-20, (H/8)-20, "Rotation", mainWindow, addRotation)
            
        
        mainWindow.show()
        
#Initialisation du mainWindow et le place théoriquement en fonciton de de la resolution de l'écran 
    app = QtWidgets.QApplication(sys.argv)    

    mainWindow = QtWidgets.QMainWindow()
    
    resolution = QtWidgets.QApplication.desktop().screenGeometry()
    mainWindow.move((resolution.width()/2)-(L/2), (resolution.height()/2)-(H/2))
    
    mainWindow.setFixedSize(L, H)
    
    mainWindow.setWindowIcon(QtGui.QIcon("images/icon.png"))
    
    logoHomeMenu = QtWidgets.QLabel(mainWindow)
    logoHomeMenu.setPixmap(QtGui.QPixmap("images/imageHomeMenu"))
    logoHomeMenu.move(10, 10)
    logoHomeMenu.resize(L-20, (H/2)-20)
    mainWindow.setWindowTitle("G.E Schématronique")
    
    mainWindow.setCentralWidget(windowEvent())
    
    windowMode(0)
#-----------------------------------------------------------   
    mainWindow.show()
    sys.exit(app.exec_())
#-----------------------------------------------------------   

main() 
