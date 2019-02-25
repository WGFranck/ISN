"""
@author: ykhima
"""
#A faire :

#-pouvoir dessiner plusieurs choses

#-les deux fenêtres pour les modes elec et logique avec un QMenu pour les differents
#composant 

#-le texte "besoin d'aide/Mode d'emploi" (peut être en ouvrant un .doc sur World ?)

#-peut être une QDockWindow pour demander la taille de la fenêtre avant de lancer main() 
#vue que l'interface est en fonction de L et H
#demander à l'utilisateur sa taille des éléments

#clique gauche pour placer et clique droit pour changer la rotation

#hypothèse : utiliser une boucle for and un newElement = tableau[tableau.lenght + 1] pour aficher tout les elements

#enlever la gomme et mettre un bouton qui restera appuyer qui sera un cable avec if x2-1>y2-y1 drawLine x1, x2 

import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QLine, QRect, QPoint

def main() :

#Taille de la fenètre MODIFIABLE 
#-et modifiable un jour par l'utilisateur 
#-toute taille disponible tant que c'est suppérieur 250 et pair
    L  = 700
    H = 700
    
#Booléan du boutton de la souris pour l'orientation des élements. A Faire !
    leftClickCanvas = False
#    rightClickCanvas = False
    leftClickCanvasExample = False
#initialisation des des positions
    cursorPos = QPoint()
    clickPos = QPoint()
    
#Taille des élements MODIFIABLE -et modifiable un jour par l'utilisateur -coefElement > 2 et coefElement pair
    coefElement = 8    
    userElement = 0
    intWindowMode = 0
    
#taille du canevas en fonction de la taille de l'écran non modifiable par l'utilisateur 
#-valeur pour intWindowMode = 0
    canvas = QRect(10, 10, L-20, (H/2)-20)
    
    canvasExample = QRect((L/2)-50, (H*8/9)-50, 100, 100) 
  
#initialisation des Button du Home Menu et du mode de création avec un tableau
    homeButton = [QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton()]
    editorButton = [QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton(), QtWidgets.QPushButton()]
#-----------------------------------------------------------     
#-----------------------------------------------------------     
#-----------------------------------------------------------
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
            nonlocal leftClickCanvas, leftClickCanvasExample, cursorPos, clickPos, userElement
            clickPos = cursorPos
            
            if not intWindowMode == 0 and canvasExample.contains(cursorPos):
                leftClickCanvas = True
                userElement = userElement + 1
                
                if userElement == len(dictElementElec) :
                    userElement = 0
                
            elif not intWindowMode == 0 and not canvas.contains(cursorPos) and not canvasExample.contains(cursorPos):
                print("vous n'êtes pas dans la zone de travail")
                leftClickCanvas = False
                    
            elif not intWindowMode == 0 and canvas.contains(cursorPos):
               leftClickCanvas = True
                
            self.update()
#-----------------------------------------------------------
         def paintEvent(self, event):
            nonlocal H, L, leftClickCanvas, clickPos, cursorPos, canvas, dictElementElec, canvasExample
            
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
            
            if leftClickCanvas and intWindowMode == 1 :
                painter.setPen(pen)
                dictElementElec[userElement](painter)
                
            elif leftClickCanvas and intWindowMode == 2:
                print("work in progress")
                leftClickCanvas = False
                                
            self.update()
#-----------------------------------------------------------
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
#-----------------------------------------------------------
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
            aireCoil = QtGui.QRegion(QRect(createPointX(-1), createPointY(-4), createPointX(1), createPointY(4)))
            zoneSave = QtGui.QRegion(QRect(createPointX(0)-2, createPointY(-4), createPointX(0)-2, createPointY(2)))
            finalZone = aireCoil.intersected(zoneSave)
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
#-----------------------------------------------------------     
#-----------------------------------------------------------     
#-----------------------------------------------------------     
#"dicitonaire" faisant l'office d'un "Switch Case" et regroupe toutes les fonctions de la class element dans un tableau, il ne reste plus qu'à faire dictElementElec[n](painter)
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
    
#Differents callBacks
    def elecMode():
        windowMode(1)

    def logicMode():
        windowMode(2)
        
    def closeProg():
        mainWindow.close()
        
    def returnHomeMenu():        
        windowMode(0)
        
#    def clearAll():   présence d'un bug quand on appui ensuite
#       nonlocal intWindowMode, leftClickCanvas, leftClickCanvasExample
#        windowMode(intWindowMode)
#        leftClickCanvas = False
#        leftClickCanvasExample = False
 
    def null():
        print("null")
#-----------------------------------------------------------
    def createButton(posX, posY, sizeX, sizeY, texte, widget, callBack) :
        
        button = QtWidgets.QPushButton(texte, widget)
        button.move(posX, posY)
        button.resize(sizeX, sizeY)
        button.clicked.connect(callBack)
        return button
    
#Les fonctions suivantes on pour but de placer les element en fonction du coef et de la souris (repère : clickPos, coefElement* x->, coefElement* y->)
    def createPointX(X):
        nonlocal clickPos, coefElement
        return clickPos.x()+X*coefElement
  
    def createPointY(Y):
        nonlocal clickPos, coefElement
        return clickPos.y()+Y*coefElement
  
    def createLine(x1, y1, x2, y2):
        nonlocal clickPos, coefElement
        
        newX1 = clickPos.x()+x1*coefElement
        newY1 = clickPos.y()+y1*coefElement
        
        newX2 = clickPos.x()+x2*coefElement
        newY2 = clickPos.y()+y2*coefElement
        
        return QLine(newX1, newY1, newX2, newY2)
#-----------------------------------------------------------  
    def windowMode(state):
        nonlocal H, L, mainWindow, canvas, homeButton, editorButton, intWindowMode
        intWindowMode = state
        
        if state == 0 :
            mainWindow.close()
            for n in range(4):
                editorButton[n].close()
            canvas = QRect(10, 10, L-20, (H/2)-20)

            homeButton[0] = createButton(10, (H*3/6), L-20, (H/6)-10, "Création de schémas électriques", mainWindow, elecMode)
            homeButton[1] = createButton(10, (H*4/6), L-20, (H/6)-10, "Création de schémas logiques", mainWindow, logicMode)
            homeButton[2] = createButton(10, (H*5/6), (L/2)-20, (H/6)-10, "Besoin d'aide ?", mainWindow, null)
            homeButton[3] = createButton((L/2)+10, (H*5/6), (L/2)-20, (H/6)-10, "Fermer l'application", mainWindow, closeProg)
        else :
            mainWindow.close()
            for n in range(4) :
                homeButton[n].close()
            canvas.setRect(10, 10, L-20, (H*7/9)-20)

            editorButton[0] = createButton(10, (H*7/9), (L/4)-20, (H/8)-20, "Gomme", mainWindow, null)
            editorButton[1] = createButton(10, (H*8/9), (L/4)-20, (H/8)-20, "Tout suppimer", mainWindow, null)
            editorButton[2] = createButton((L*3/4), (H*7/9), (L/4)-20, (H/8)-20, "Retour", mainWindow, returnHomeMenu)    
            editorButton[3] = createButton((L*3/4), (H*8/9), (L/4)-20, (H/8)-20, "Fermer l'application", mainWindow, closeProg)
        
        mainWindow.show()
#-----------------------------------------------------------
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
#Fenètre suplémantaire qui devra contenir le texte de la partie "besoin d'aide"
#    interface = QtWidgets.QDockWidget("Guide d'utilisation")
#    interface.resize(L, H/2)
#    interface.move(0, 0)
#-----------------------------------------------------------   
    mainWindow.show()
#    interface.show()
    sys.exit(app.exec_())
#-----------------------------------------------------------   
    
main() 
