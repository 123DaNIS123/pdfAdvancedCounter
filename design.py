from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from main import calculate_all
import os


# class Widget1(QWidget):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent=parent)
#         lay = QVBoxLayout(self)
#         for i in range(4):
#             lay.addWidget(QPushButton("{}".format(i)))

class stackedExample(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.paths = [os.path.dirname(os.path.realpath(__file__)), os.path.dirname(os.path.realpath(__file__))]
        self.setWindowTitle("PDF Pages Counter")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), "icon.ico")))
        lay = QVBoxLayout(self)
        # self.Stack = QStackedWidget()
        # self.Stack.addWidget(Widget1())

        btnWhere = QPushButton("Choose folder where your pdf files are")
        btnWhere.clicked.connect(lambda: self.changeParam(0))
        btnRes = QPushButton("Choose folder where to store result.txt")
        btnRes.clicked.connect(lambda: self.changeParam(1))
        self.textbox = QLineEdit(self)
        self.textbox.setText("26")
        self.textbox.setToolTip("Acceptable error in pixels, default=26")
        self.checkSubs = QCheckBox(self)
        self.checkSubs.setText("check subfolders")
        self.checkSubs.setToolTip("Defines whether to check subfolders' pdf files or not")
        btnLayout1 = QHBoxLayout()
        btnLayout1.addWidget(btnWhere)
        btnLayout1.addWidget(btnRes)
        btnLayout2 = QHBoxLayout()
        btnLayout2.addWidget(self.textbox)
        btnLayout2.addWidget(self.checkSubs)
        btnLayout3 = QHBoxLayout()
        btnCalc = QPushButton("Calculate")
        btnCalc.clicked.connect(lambda: self.calculate())
        btnLayout3.addWidget(btnCalc)
        self.statusText = QLabel(self)
        self.statusText.setText("Everything is fine:)")
        self.statusText.setToolTip("shows the status of program execution")
        btnLayout4 = QHBoxLayout()
        btnLayout4.addWidget(self.statusText)

        lay.addLayout(btnLayout1)
        lay.addLayout(btnLayout2)
        lay.addLayout(btnLayout3)
        lay.addLayout(btnLayout4)
    
    def changeParam(self, n):
        self.paths[n] = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    
    def calculate(self):
        try:
            calculate_all(self.paths[0], self.paths[1], int(self.textbox.text()), self.checkSubs.isChecked())
            self.statusText.setText("Everything is fine:)     Check results in result.txt")
        except ValueError as valErr:
            self.statusText.setText("Write an integer as an error value!")
        except RecursionError as recErr:
            self.statusText.setText("Too many subfolders to check. Select another folder or manage the current one")
        except Exception as e:
            self.statusText.setText(repr(e))



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = stackedExample()
    w.show()
    sys.exit(app.exec_())
