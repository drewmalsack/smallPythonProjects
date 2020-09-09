import sqlite3

connection = sqlite3.connect("contacts.db")


def add_contact():
    contact_add = input("Enter contact in form of [Name, Number, Email], without brackets, or exit to cancel")
    if contact_add.lower == "exit":
        return
    contact_list = contact_add.split(",")
    for i in range(len(contact_list)):
        contact_list[i].strip()
    cursor.execute("INSERT INTO Contacts VALUES ('"+contact_list[0]+"', '"+contact_list[1]+"', '"+contact_list[2]+"')")


def search_contact():
    contact_search = input("Enter name of contact you would like to lookup, or exit to cancel.")
    if contact_search.lower == "exit":
        return
    rows = cursor.execute("SELECT * FROM 'Contacts' WHERE name='"+contact_search+"'").fetchone()
    print(rows)


def delete_contact():
    contact_rem = input("Enter name of contact you would like to delete, search to see contacts, or exit to cancel.")
    while contact_rem == "search" or contact_rem == "exit":
        if contact_rem == "exit":
            return
        elif contact_rem == "search":
            rows = cursor.execute("SELECT name, number, email FROM 'Contacts'").fetchall()
            print(rows)
            contact_rem = input(
                "Enter name of contact you would like to delete, search to see contacts, or exit to cancel.")
    cursor.execute("DELETE FROM 'Contacts' Where name = '"+contact_rem+"'")


def commit():
    connection.commit()


def edit_contact():

    contact_edit = input("Enter name of contact you would like to edit, search to see contacts, or exit to cancel.")
    while contact_edit == "search" or contact_edit == "exit":
        if contact_edit == "exit":
            return
        elif contact_edit == "search":
            rows = cursor.execute("SELECT name, number, email FROM 'Contacts'").fetchall()
            print(rows)
            contact_edit = input("Enter name of contact you would like to edit, search to see contacts,"
                                 " or exit to cancel.")

    rows = cursor.execute("SELECT * FROM 'Contacts' WHERE name='" + contact_edit + "'").fetchone()
    print(rows)
    temp = contact_edit
    contact_edit = input("Enter new info in format [name, number, email] without brackets, or exit to cancel")
    if contact_edit == "exit":
        return

    contact_list = contact_edit.split(",")
    for i in range(len(contact_list)):
        contact_list[i].strip()

    cursor.execute("INSERT INTO Contacts VALUES ('"+contact_list[0]+"', '"+contact_list[1]+"', '"+contact_list[2]+"')")
    cursor.execute("DELETE FROM 'Contacts' Where name = '" + temp + "'")


if __name__ == '__main__':
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Contacts (name, number, email)''')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Contacts';")
    while True:
        print("1 for add contact")
        print("2 for search contact")
        print("3 for delete contact")
        print("4 for edit contact")
        print("5 to commit changes")
        print("6 to exit")
        choice = input("Enter choice")
        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            edit_contact()
        elif choice == "5":
            commit()
        else:
            connection.close()
            break
