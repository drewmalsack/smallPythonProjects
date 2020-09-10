import sqlite3
import sys
import re
from PyQt5 import QtCore, QtWidgets

connection = sqlite3.connect("contacts.db")
cursor = connection.cursor()


# main window with buttons to other menus
class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        layout = QtWidgets.QGridLayout()

        # Creating buttons for Main Window to access other menus and closing program
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
        self.exitButton = QtWidgets.QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)


        # adding to layout
        layout.addWidget(self.insertButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.searchButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.commitButton)
        layout.addWidget(self.exitButton)

        self.setLayout(layout)

    def send_control(self, text):
        self.switch_window.emit(text)

    def commit(self):
        connection.commit()
        self.confirmw = ConfirmWindow("Commit")
        self.confirmw.show()


# window for inserting into database
class InsertWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        layout = QtWidgets.QGridLayout()

        self.name_line = QtWidgets.QLineEdit()

        self.number_line = QtWidgets.QLineEdit()

        self.email_line = QtWidgets.QLineEdit()

        self.name_label = QtWidgets.QLabel("Name")
        self.number_label = QtWidgets.QLabel("Number")
        self.email_label = QtWidgets.QLabel("Email")

        self.insertButton = QtWidgets.QPushButton("Insert")
        self.insertButton.clicked.connect(self.sql_insert)

        self.backButton = QtWidgets.QPushButton("Back")
        self.backButton.clicked.connect(self.send_control)

        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_line, 0, 1)
        layout.addWidget(self.number_label, 1, 0)
        layout.addWidget(self.number_line, 1, 1)
        layout.addWidget(self.email_label, 2, 0)
        layout.addWidget(self.email_line, 2, 1)
        layout.addWidget(self.insertButton, 3, 0)
        layout.addWidget(self.backButton, 3, 1)

        self.setLayout(layout)

    # handles checking input text for format and inserting into database
    def sql_insert(self):
        pattern = re.compile(r'[a-z]+[,]\s[0-9a-z]+[,]\s[a-z0-9]+[@][a-z]+[.][a-z]+', re.IGNORECASE)
        contact_add = self.name_line.text()+", "+self.number_line.text()+", "+self.email_line.text()
        if re.search(pattern, contact_add):
            contact_list = contact_add.split(",")
            for i in range(len(contact_list)):
                contact_list[i].strip()
            cursor.execute(
                "INSERT INTO Contacts VALUES ('" + contact_list[0] + "', '" + contact_list[1] + "', '" + contact_list[
                    2] + "')")
            self.confirmw = ConfirmWindow("Insert")
            self.confirmw.show()
        else:
            self.confirmw = ConfirmWindow("Wrong")
            self.confirmw.show()

    # sends signal to controller to open relevent window
    def send_control(self):
        self.switch_window.emit()


# window confirms action, can be opened from multiple other windows and shows relevant info based on which window opened
# it
class ConfirmWindow(QtWidgets.QWidget):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Confirm")

        layout = QtWidgets.QGridLayout()

        self.confirm_label = QtWidgets.QLabel()

        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.close)

        # if statements to control what to say depending on what window opened this window
        if text == "Insert":
            self.confirm_label.setText("Contact added Successfully.")
        elif text == "Delete":
            self.confirm_label.setText("Contact Deleted.")
        elif text == "Commit":
            self.confirm_label.setText("Changes Committed.")
        else:
            self.confirm_label.setText("Input is in wrong format")

        layout.addWidget(self.confirm_label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)


# window for deleting from database
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

    # handles deleting from database and eventually making sure text format is right
    def sql_delete(self):
        contact_rem = self.line_edit.text()
        cursor.execute("DELETE FROM 'Contacts' Where name = '" + contact_rem + "'")
        self.confirmw = ConfirmWindow("Delete")
        self.confirmw.show()

    # sends to controller to handle which window to open
    def send_control(self):
        self.switch_window.emit()


# window to search database
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

    # handles searching database and eventually text formatting
    def sql_search(self):
        contact_search = self.line_edit.text()
        rows = str(cursor.execute("SELECT * FROM 'Contacts' WHERE name='" + contact_search + "'").fetchall())
        #print(str(rows))
        if rows != "None":
            rows = rows.replace('(', "")
            rows = rows.replace(')', "")
            rows = rows.replace('\'', "")
        self.send_control("SearchR"+rows)

    # send to controller to open the next window
    def send_control(self, text):
        self.switch_window.emit(text)


# window called from SearchWindow to show results from search, only works with one entry. may expand to see multiple
# entries in the future
class ShowResults(QtWidgets.QWidget):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("SQLite GUI")

        number = ""
        email = ""

        # formatting string received from other function
        rows = text.replace("SearchR", "")
        rows = rows.replace("[", "")
        rows = rows.replace("]", "")
        rows = rows.replace(" ", "")

        # additional formatting and cutting string into list
        if rows != "None":
            contact_list = rows.split(",")
            for i in range(len(contact_list)):
                contact_list[i].lstrip()
            for i in range(int(len(contact_list)/3)):
                number = number + contact_list[3*i+1] + ","
                email = email + contact_list[3*i+2] + ","
            name = contact_list[0]
        else:
            name = rows
            number = rows
            email = rows

        # taking strings from contact_list and splitting them into specific lists for drop down menus
        number_list = number.split(",")
        email_list = email.split(",")

        layout = QtWidgets.QGridLayout()

        # labels for menu
        self.name_label = QtWidgets.QLabel("Name")
        self.number_label = QtWidgets.QLabel("Number")
        self.email_label = QtWidgets.QLabel("Email")

        # line edit for name and drop down lists for number and email fields
        self.name_line = QtWidgets.QLineEdit()
        self.name_line.setText(name)
        self.name_line.setReadOnly(True)

        # loops for adding content into specific drop down lists
        self.number_box = QtWidgets.QComboBox()
        for i in range(len(number_list)-1):
            self.number_box.addItem(number_list[i])
        #self.number_line.setText(number)
        #self.number_line.setReadOnly(True)

        self.email_box = QtWidgets.QComboBox()
        for i in range(len(email_list)-1):
            self.email_box.addItem(email_list[i])
        #self.email_line.setText(email)
        #self.email_line.setReadOnly(True)

        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.close)

        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_line, 0, 1)

        layout.addWidget(self.number_label, 1, 0)
        layout.addWidget(self.number_box, 1, 1)

        layout.addWidget(self.email_label, 2, 0)
        layout.addWidget(self.email_box, 2, 1)

        layout.addWidget(self.ok_button, 3, 1)

        self.setLayout(layout)


# Controller class receives signals from other window classes and controller opening and closing of windows
class Controller:

    def __init__(self):
        pass

    # receives text from current window and sends control to method to open next window. closes current window if
    # necessary
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
            if text[5] == "I":
                self.insertw.close()
            elif text[5] == "D":
                self.deletew.close()
            elif text[5] == "S":
                self.searchw.close()
            self.show_main()

    # these methods create instances of window classes they are tied to, handle receiving of signals from those classes
    # opens the window and send signals to choose_window method to choose next window to open
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


# main method
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
