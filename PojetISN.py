"""
@author: ykhima
"""
#A faire :

#-avoir plusieur élements en même temps

#-le texte "besoin d'aide/Mode d'emploi" (peut être en ouvrant un .doc sur World ?)

#-peut être une QDockWindow pour demander la taille de la fenêtre et le coefElement avant de lancer main() 
#vue que l'interface est en fonction de L et H

#programmer la rotation

#hypothèse : utiliser une boucle for et un newElement = turple[len(turple.lenght) + 1] pour aficher tout les elements

#-Appuyer sur shift quand lineMode is checked pour faire des lignes horizontal ou verticale

#utiliser un QDockWidget pour le texte de "besoin d'aide"

import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QLine, QRect, QPoint


def main() :

#Taille de la fenètre MODIFIABLE dans le programme
#-et modifiable un jour par l'utilisateur 
#-toute taille disponible tant que c'est suppérieur 250 et pair
    L  = 700
    H = 800
    
#Booléan du boutton de la souris pour la position des élements.
    clickCanvas = False
    
#l'utilisateur doit clicker une prmière fois pour appeler un élément puis un second click pour le placer sur le canevas
    initClick = False
#initialisation des positions
    cursorPos = QPoint()
    clickPos = QPoint()
    
#Taille des élements MODIFIABLE dans le programme
#-et modifiable un jour par l'utilisateur 
#-coefElement >= 2 et coefElement pair et c'est lisible quand c'est >=6
    coefElement = 8 
    
#élement choisit par l'utilisateur    
    userElement = 0
    
    intWindowMode = 0
    
    lineMode = False
#taille du canevas en fonction de la taille de l'écran non modifiable par l'utilisateur 
#-valeur pour intWindowMode = 0 servira pour afficher une image
    canvas = QRect(10, 10, L-20, (H/2)-20)
#Canvas Example est le canvas qui permet de changer d'element ou changer la rotation (théoriquement)    
    canvasExample = QRect((L/2)-50, (H*8/9)-50, L/7, H/7) 
  
#initialisation des Button du Home Menu et du mode de création avec un tableau
    homeButton = [QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton()]
    editorButton = [QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton()]
#-----------------------------------------------------------     
#-----------------------------------------------------------     
#class des différents évenement de mainWindow
    class windowEvent(QtWidgets.QMainWindow):
#-----------------------------------------------------------
         def __init__(self):
            super().__init__()
            self.setMouseTracking(True)
#-----------------------------------------------------------
         def mouseMoveEvent(self, event):
            nonlocal cursorPos
            cursorPos = event.pos()

            self.update()
#-----------------------------------------------------------            
         def mousePressEvent(self, event):
            nonlocal clickCanvas, initClick, cursorPos, clickPos, userElement
            clickPos = cursorPos
            
            if not intWindowMode == 0 and canvasExample.contains(cursorPos):
                clickCanvas = True
                userElement = userElement + 1
                initClick = False
                
                if userElement == len(dictElementElec) and intWindowMode == 1:
                    userElement = 0
                elif userElement == len(dictElementLogic) and intWindowMode == 2:
                    userElement =0
                
            elif not intWindowMode == 0 and canvas.contains(cursorPos):
               clickCanvas = True
               initClick = not initClick
               
            elif not intWindowMode == 0 and not canvas.contains(cursorPos) and not canvasExample.contains(cursorPos):
                print("vous n'êtes pas dans la zone de travail")
                clickCanvas = False
                
            self.update()

#-----------------------------------------------------------
         def paintEvent(self, event):
            nonlocal H, L, clickCanvas, initClick, clickPos, cursorPos, canvas, dictElementElec, canvasExample, lineMode
            
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
                
            if initClick:
                clickPos = cursorPos
            
            if clickCanvas and intWindowMode == 1 and not lineMode:
                dictElementElec[userElement](painter)
                
            elif clickCanvas and intWindowMode == 2 and not lineMode:
                dictElementLogic[userElement](painter)
            
            elif lineMode and clickCanvas and canvas.contains(clickPos) and (intWindowMode == 2 or intWindowMode == 1):
                painter.drawLine(clickPos.x(), clickPos.y(), cursorPos.x(), cursorPos.y())
            
            self.update()
#-----------------------------------------------------------
#-----------------------------------------------------------   
#Les class des élements a pour but de dessiner les élements en fonction de la souris
    class elementElec(QPainter):        
#-----------------------------------------------------------     
        def resistance(self):
            #base
            self.drawRect(createPointX(-1), createPointY(-2), 2*coefElement, 4*coefElement)
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
#-----------------------------------------------------------
        def generator(self):
            #base
            self.drawEllipse(createPointX(-2), createPointY(-2), 4*coefElement, 4*coefElement)
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
            
            #definition de la zone à concerver (pour avoir un arc de cercle)
            regElement = QtGui.QRegion(QRect(createPointX(-0.5), createPointY(-4), 1*coefElement, 8*coefElement))
            saveZone = QtGui.QRegion(QRect(createPointX(0)-2, createPointY(-4), 0.5*coefElement+4, 8*coefElement))
            finalZone = regElement.intersected(saveZone)
            #définition de la zone de dessin
            self.setClipRegion(finalZone)
            #cable
            self.drawLine(createLine(0, -4, 0, -2))
            self.drawLine(createLine(0, 4, 0, 2))
            #base (avec le surplus)
            self.drawEllipse(createPointX(-0.5), createPointY(-2), 1*coefElement, 1*coefElement)
            self.drawEllipse(createPointX(-0.5), createPointY(-1), 1*coefElement, 1*coefElement)
            self.drawEllipse(createPointX(-0.5), createPointY(0), 1*coefElement, 1*coefElement)
            self.drawEllipse(createPointX(-0.5), createPointY(1), 1*coefElement, 1*coefElement)
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
#----------------------------------------------------------     
#-----------------------------------------------------------     
#-----------------------------------------------------------     
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
           8 : elementElec.AOP, }
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
            self.drawEllipse(createPointX(-0.5), createPointY(-2.5), 1*coefElement, 1*coefElement)
            
        def orGate(self):
            
            #définition de la zone de dessin de la base
            regElement = QtGui.QRegion(QRect(createPointX(-2)-2, createPointY(-4)-2, 4*coefElement+4, 8*coefElement+4))
            saveZone = QtGui.QRegion(QRect(createPointX(-2)-2, createPointY(-2)-2, 4*coefElement+4, 4*coefElement+4))
            regBase = regElement.intersected(saveZone)
            self.setClipRegion(regBase)
            #base
            self.drawEllipse(createPointX(-2), createPointY(-2), 4*coefElement, 8*coefElement)
            self.drawEllipse(createPointX(-2), createPointY(1.5), 4*coefElement, 2*coefElement)
            #cable
            self.setClipRegion(regElement)
            self.drawLine(createLine(0, -2, 0, -4))
            self.drawLine(createLine(-1, 1.5, -1, 4))
            self.drawLine(createLine(1, 1.5, 1, 4))
            
        def norGate(self):
            elementLogic.orGate(self)
            self.drawEllipse(createPointX(-0.5), createPointY(-3), 1*coefElement, 1*coefElement)
        
        def xorGate(self):
            elementLogic.orGate(self)
            
            regElement = QtGui.QRegion(QRect(createPointX(-2)-2, createPointY(-4)-2, 4*coefElement+4, 8*coefElement+4))
            saveZone = QtGui.QRegion(QRect(createPointX(-2)-2, createPointY(2)-2, 4*coefElement+4, 1*coefElement))
            regBase = regElement.intersected(saveZone)
            
            self.setClipRegion(regBase)
            
            self.drawEllipse(createPointX(-2), createPointY(2), 4*coefElement, 2*coefElement)
            
        def nxorGate(self):
            elementLogic.norGate(self)
            elementLogic.xorGate(self)
            
            
        def andGate(self):
            
            regElement = QtGui.QRegion(QRect(createPointX(-2)-2, createPointY(-4)-2, 4*coefElement+4, 8*coefElement+4))
            saveZone = QtGui.QRegion(QRect(createPointX(-2)-2, createPointY(-2)-2, 4*coefElement+4, 2*coefElement+4))
            regBase = regElement.intersected(saveZone)
            self.setClipRegion(regBase)
            #base
            self.drawEllipse(createPointX(-2), createPointY(-1), 4*coefElement, 2*coefElement)
            self.setClipRegion(regElement)
            self.drawLine(createLine(-2, 0, -2, 2))
            self.drawLine(createLine(-2, 2, 2, 2))
            self.drawLine(createLine(2, 2, 2, 0))
            #cable
            self.drawLine(createLine(-1, 2, -1, 4))
            self.drawLine(createLine(1, 2, 1, 4))
            self.drawLine(createLine(0, -1, 0, -4))
            
        def nandGate(self):
            elementLogic.andGate(self)
            self.drawEllipse(createPointX(-0.5), createPointY(-2), 1*coefElement, 1*coefElement)
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
           
#Differents callBacks
    def elecMode():
        windowMode(1)

    def logicMode():
        windowMode(2)
        
    def closeProg():
        mainWindow.close()
        
    def returnHomeMenu():
        nonlocal userElement, clickCanvas, initClick, lineMode, clickCanvas
        userElement = 0
        clickCanvas = False
        initClick = False
        lineMode = False
        windowMode(0)
        
    def buttonlineMode():
        nonlocal lineMode, initClick, editorButton, clickCanvas

        clickCanvas = False
        if editorButton[0].isChecked():
            lineMode = True
            initClick = True
            
        else :
            lineMode = False
            initClick = False
    def null():
        print("null")
#-----------------------------------------------------------
    def createButton(posX, posY, sizeX, sizeY, texte, widget, callBack) :
        
        button = QtWidgets.QPushButton(texte, widget)
        button.move(posX, posY)
        button.resize(sizeX, sizeY)
        button.clicked.connect(callBack)
        return button
    
#Les fonctions suivantes ont pour but de créer les élements en fonction du coef et de la souris (repère : clickPos, coefElement* x->, coefElement* y->)
    def createPointX(X):
        nonlocal clickPos, coefElement
        return clickPos.x()+X*coefElement
  
    def createPointY(Y):
        nonlocal clickPos, coefElement
        return clickPos.y()+Y*coefElement
  
    def createLine(x1, y1, x2, y2):       
        return QLine(createPointX(x1), createPointY(y1), createPointX(x2), createPointY(y2))
    
#cette fonction a pour but de regler les bouttons des deux modes (home et création)
    def windowMode(state):
        nonlocal H, L, mainWindow, canvas, homeButton, editorButton, intWindowMode
        intWindowMode = state
        
        if state == 0 :
            mainWindow.close()
            for n in range(len(homeButton)):
                editorButton[n].close()
            canvas = QRect(10, 10, L-20, (H/2)-20)

            homeButton[0] = createButton(10, (H*3/6), L-20, (H/6)-10, "Création de schémas électriques", mainWindow, elecMode)
            homeButton[1] = createButton(10, (H*4/6), L-20, (H/6)-10, "Création de schémas logiques", mainWindow, logicMode)
            homeButton[2] = createButton(10, (H*5/6), (L/2)-20, (H/6)-10, "Besoin d'aide ?", mainWindow, null)
            homeButton[3] = createButton((L/2)+10, (H*5/6), (L/2)-20, (H/6)-10, "Fermer l'application", mainWindow, closeProg)
        else :
            mainWindow.close()
            for n in range(len(homeButton)) :
                homeButton[n].close()
            canvas.setRect(10, 10, L-20, (H*7/9)-20)

            editorButton[0] = createButton(10, (H*7/9), (L/4)-20, (H/8)-20, "Cable", mainWindow, buttonlineMode)
            editorButton[0].setCheckable(True)
            editorButton[1] = createButton(10, (H*8/9), (L/4)-20, (H/8)-20, "Tout suppimer", mainWindow, null)
            editorButton[2] = createButton((L*3/4), (H*7/9), (L/4)-20, (H/8)-20, "Retour", mainWindow, returnHomeMenu)    
            editorButton[3] = createButton((L*3/4), (H*8/9), (L/4)-20, (H/8)-20, "Fermer l'application", mainWindow, closeProg)
        
        mainWindow.show()
        
#Initialisation du mainWindow et le place théoriquement en fonciton de de la resolution de l'écran 
    app = QtWidgets.QApplication(sys.argv)    

    mainWindow = QtWidgets.QMainWindow()
    
    resolution = QtWidgets.QApplication.desktop().screenGeometry()
    mainWindow.move((resolution.width()/2)-(L/2), (resolution.height()/2)-(H/2))
    
    mainWindow.setFixedSize(L, H)
    
    mainWindow.setWindowIcon(QtGui.QIcon("icon.png"))
    
    mainWindow.setWindowTitle("G.E Schématronique")
    
    mainWindow.setCentralWidget(windowEvent())
    
    windowMode(0)
#-----------------------------------------------------------   
    mainWindow.show()
    sys.exit(app.exec_())
#-----------------------------------------------------------   
    
main() 
