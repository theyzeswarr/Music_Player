import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem
import sqlite3

class ContactListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact List")
        self.setGeometry(200, 200, 500, 400)
        self.setup_ui()
        self.create_connection()
        self.create_table()

    def setup_ui(self):
        self.name_label = QLabel("Name:", self)
        self.name_label.move(20, 20)
        self.name_input = QLineEdit(self)
        self.name_input.move(100, 20)

        self.phone_label = QLabel("Phone:", self)
        self.phone_label.move(20, 60)
        self.phone_input = QLineEdit(self)
        self.phone_input.move(100, 60)

        self.email_label = QLabel("Email:", self)
        self.email_label.move(20, 100)
        self.email_input = QLineEdit(self)
        self.email_input.move(100, 100)

        self.add_button = QPushButton("Add", self)
        self.add_button.move(20, 140)
        self.add_button.clicked.connect(self.add_contact)

        self.show_button = QPushButton("Show Contacts", self)
        self.show_button.move(100, 140)
        self.show_button.clicked.connect(self.show_contacts)

        self.contact_table = QTableWidget(self)
        self.contact_table.setGeometry(20, 180, 460, 200)
        self.contact_table.setColumnCount(3)
        self.contact_table.setHorizontalHeaderLabels(["Name", "Phone", "Email"])

    def create_connection(self):
        self.conn = sqlite3.connect("contacts.db")
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS contacts (name TEXT, phone TEXT, email TEXT)"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if name and phone and email:
            insert_query = "INSERT INTO contacts VALUES (?, ?, ?)"
            self.cursor.execute(insert_query, (name, phone, email))
            self.conn.commit()
            self.show_message_box("Success", "Contact added successfully!")
            self.clear_inputs()
        else:
            self.show_message_box("Error", "Please fill in all the fields.")

    def show_contacts(self):
        self.contact_table.setRowCount(0)
        select_query = "SELECT * FROM contacts"
        contacts = self.cursor.execute(select_query).fetchall()

        for row_number, contact in enumerate(contacts):
            self.contact_table.insertRow(row_number)
            for column_number, data in enumerate(contact):
                self.contact_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    contact_list_app = ContactListApp()
    contact_list_app.show()
    sys.exit(app.exec_())
