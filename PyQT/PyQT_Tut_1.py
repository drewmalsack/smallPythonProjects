from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 320)
    win.setWindowTitle("Tutorial_1")

    label = QtWidgets.QLabel(win)
    label.setText("Test Label Text")
    label.move(50, 50)

    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
