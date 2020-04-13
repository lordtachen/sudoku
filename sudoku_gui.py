from PySide2.QtWidgets import QComboBox, QAction, QMainWindow, QApplication, QWidget, QLabel, QPushButton, QGridLayout, QTextEdit,QVBoxLayout, QFrame, QWidgetItem
import sys
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(300,300,500,500)
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)

        self.setWindowIcon(QIcon("images/index.png"))
        self.createMenu()
        self.setCentralWidget(self.createBoard())

        self.show()

    def createBoard(self):
        wid=QFrame(self)
        gridlayout = QGridLayout()
        gridlayout.setSpacing(0)
        box_list=[]
        for i in range(3):
            for j in range(3):
                box_list.append(self.createSBoard())
                #box_list[-1].setFixedSize(50,50)
                #label_list[-1].setAlignment(Qt.AlignCenter)
                #label_list[-1].setFrameStyle(QFrame.Box)
                #label_list[-1].setLineWidth(1)
                gridlayout.addWidget(box_list[-1],i,j)
        #self.setLayout(gridlayout)
        wid.setLayout(gridlayout)
        return wid

    def createSBoard(self):
        wid=QFrame(self)
        wid.setFrameStyle(QFrame.Box)
        wid.setLineWidth(2)
        gridlayout = QGridLayout()
        gridlayout.setSpacing(0)
        label_list=[]
        for i in range(3):
            for j in range(3):
                #label_list.append(QPushButton("{},{}".format(i,j),self))
                qcb=QComboBox(self)
                qcb.addItems([str(i) for i in range(1,10)])
                label_list.append(qcb)
                label_list[-1].setFixedSize(50,50)
                #label_list[-1].setAlignment(Qt.AlignCenter)
                #label_list[-1].setFrameStyle(QFrame.Box)
                #label_list[-1].setLineWidth(1)
                gridlayout.addWidget(label_list[-1],i,j)
        wid.setLayout(gridlayout)
        return wid

    def createMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        loadAction = QAction("Load",self)
        fileMenu.addAction(loadAction)
        newAction = QAction("New",self)
        fileMenu.addAction(newAction)
        solveAction = QAction("Solve",self)
        fileMenu.addAction(solveAction)
        loadAction.triggered.connect(self.loadSudoku)
    def loadSudoku(self):
        pass
if __name__=='__main__':
    sudokuApp = QApplication(sys.argv)
    window=Window()

    sudokuApp.exec_()
    sys.exit(0)