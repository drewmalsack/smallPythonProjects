import sqlite3
import sys
from PyQt5 import QtCore, QtWidgets

connection = sqlite3.connect("contacts.db")
cursor = connection.cursor()


class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        layout = QtWidgets.QGridLayout()

        self.insertButton = QtWidgets.QPushButton("Insert")
        self.insertButton.clicked.connect(lambda: self.send_control(self.insertButton.text()))
        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.deleteButton.clicked.connect(lambda: self.send_control(self.deleteButton.text()))
        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.clicked.connect(lambda: self.send_control(self.searchButton.text()))
        self.editButton = QtWidgets.QPushButton("Edit")
        self.editButton.clicked.connect(lambda: self.send_control(self.editButton.text()))
        self.commitButton = QtWidgets.QPushButton("Commit")
        self.commitButton.clicked.connect(self.commit)

        layout.addWidget(self.insertButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.searchButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.commitButton)

        self.setLayout(layout)

    def send_control(self, text):
        self.switch_window.emit(text)

    def commit(self):
        connection.commit()


class InsertWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setText("Format: {name, number, email} without brackets")

        self.insertButton = QtWidgets.QPushButton("Insert")
        self.insertButton.clicked.connect(self.sql_insert)

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.clicked.connect(self.send_control)

        layout.addWidget(self.insertButton)
        layout.addWidget(self.backButton)
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

    def sql_insert(self):
        contact_add = self.line_edit.text()
        contact_list = contact_add.split(",")
        for i in range(len(contact_list)):
            contact_list[i].strip()
        cursor.execute(
            "INSERT INTO Contacts VALUES ('" + contact_list[0] + "', '" + contact_list[1] + "', '" + contact_list[
                2] + "')")

    def send_control(self):
        self.switch_window.emit()


class DeleteWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setText("Enter name of contact you want to remove.")

        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.deleteButton.clicked.connect(self.sql_delete)

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.clicked.connect(self.send_control)

        layout.addWidget(self.deleteButton)
        layout.addWidget(self.backButton)
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

    def sql_delete(self):
        contact_rem = self.line_edit.text()
        cursor.execute("DELETE FROM 'Contacts' Where name = '" + contact_rem + "'")

    def send_control(self):
        self.switch_window.emit()


class SearchWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        layout = QtWidgets.QGridLayout()

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setText("Search by name")

        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.clicked.connect(self.sql_search)

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.clicked.connect(lambda: self.send_control("Back S"))

        layout.addWidget(self.searchButton)
        layout.addWidget(self.backButton)
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

    def sql_search(self):
        contact_search = self.line_edit.text()
        rows = str(cursor.execute("SELECT * FROM 'Contacts' WHERE name='" + contact_search + "'").fetchone())
        self.line_edit.setText(str(rows))
        if rows != "None":
            rows = rows.replace('(', "")
            rows = rows.replace(')', "")
            rows = rows.replace('\'', "")
        self.send_control("SearchR"+rows)

    def send_control(self, text):
        self.switch_window.emit(text)


class ShowResults(QtWidgets.QWidget):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        rows = text.replace("SearchR", "")
        if rows != "None":
            contact_list = rows.split(",")
            for i in range(len(contact_list)):
                contact_list[i].lstrip()
            name = contact_list[0]
            number = contact_list[1]
            email = contact_list[2]
        else:
            name = rows
            number = rows
            email = rows

        layout = QtWidgets.QGridLayout()

        self.name_label = QtWidgets.QLabel("Name")
        self.number_label = QtWidgets.QLabel("Number")
        self.email_label = QtWidgets.QLabel("Email")

        self.name_line = QtWidgets.QLineEdit()
        self.name_line.setText(name)
        self.name_line.setReadOnly(True)

        self.number_line = QtWidgets.QLineEdit()
        self.number_line.setText(number)
        self.number_line.setReadOnly(True)

        self.email_line = QtWidgets.QLineEdit()
        self.email_line.setText(email)
        self.email_line.setReadOnly(True)

        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_line, 0, 1)

        layout.addWidget(self.number_label, 1, 0)
        layout.addWidget(self.number_line, 1, 1)

        layout.addWidget(self.email_label, 2, 0)
        layout.addWidget(self.email_line, 2, 1)

        self.setLayout(layout)


class Controller:

    def __init__(self):
        pass

    def choose_window(self, text):
        if text == "Insert":
            self.mainw.close()
            self.show_insert()
        elif text == "Delete":
            self.mainw.close()
            self.show_delete()
        elif text == "Search":
            self.mainw.close()
            self.show_search()
        elif "SearchR" in text:
            self.show_searchr(text)
        elif "Back" in text:
            print(text[5])
            if text[5] == "I":
                self.insertw.close()
            elif text[5] == "D":
                self.deletew.close()
            elif text[5] == "S":
                self.searchw.close()
            self.show_main()

    def show_main(self):
        self.mainw = MainWindow()
        self.mainw.switch_window.connect(self.choose_window)
        self.mainw.show()

    def show_insert(self):
        self.insertw = InsertWindow()
        self.insertw.switch_window.connect(lambda: self.choose_window("Back I"))
        self.insertw.show()

    def show_delete(self):
        self.deletew = DeleteWindow()
        self.deletew.switch_window.connect(lambda: self.choose_window("Back D"))
        self.deletew.show()

    def show_search(self):
        self.searchw = SearchWindow()
        self.searchw.switch_window.connect(self.choose_window)
        self.searchw.show()

    def show_searchr(self, text):
        self.searchr = ShowResults(text)
        self.searchr.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
