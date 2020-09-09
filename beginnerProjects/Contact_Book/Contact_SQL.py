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
    rows = cursor.execute("SELECT name, number, email FROM 'Contacts'").fetchall()
    print(rows)


def search_contact():
    contact_search = input("Enter name of contact you would like to lookup, or exit to cancel.")
    if contact_search.lower == "exit":
        return
    rows = cursor.execute("SELECT * FROM 'Contacts' WHERE name='"+contact_search+"'").fetchone()
    print(rows)


def delete_contact():
    rows = cursor.execute("SELECT name, number, email FROM 'Contacts'").fetchall()
    print(rows)
    contact_rem = input("Enter name of contact you would like to delete, or exit to cancel.")
    if contact_rem.lower == "exit":
        return
    cursor.execute("DELETE FROM 'Contacts' Where name = '"+contact_rem+"'")


def commit():
    connection.commit()


if __name__ == '__main__':
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Contacts (name, number, email)''')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Contacts';")
    while True:
        print("1 for add contact")
        print("2 for search contact")
        print("3 for delete contact")
        print("4 commit changes")
        print("5 to exit")
        choice = input("Enter choice")
        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            commit()
        else:
            break
