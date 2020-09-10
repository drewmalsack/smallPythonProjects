from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 300, 320)
        self.setWindowTitle("Tutorial_1")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Test Label Text")
        self.label.move(50, 50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Click me")
        self.b1.clicked.connect(self.searchUI)

    def clicked(self):
        self.label.setText("You Pressed the Button")
        self.update()

    def update(self):
        self.label.adjustSize()

    def searchUI(self):
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Initial View")
        self.b2.clicked.connect(self.initUI)


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
