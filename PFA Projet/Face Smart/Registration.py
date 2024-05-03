import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QComboBox

class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration")
        self.setGeometry(700, 400, 500, 200)

        layout = QVBoxLayout()

        self.Fname_input = QLineEdit()
        self.Lname_input = QLineEdit()
        self.department_combo = QComboBox()
        self.department_combo.addItems(["1", "2", "3"])
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.email_input = QLineEdit()

        register_button = QPushButton("Register")

        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.Fname_input)
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.Lname_input)
        layout.addWidget(QLabel("Department:"))
        layout.addWidget(self.department_combo)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(register_button)
        register_button.clicked.connect(self.register)

        self.setLayout(layout)

    def register(self):
        self.conn = sqlite3.connect('gestion_des_employes.db')
        self.cursor = self.conn.cursor()
        first_name = self.Fname_input.text()
        last_name = self.Lname_input.text()
        department = self.department_combo.currentText()
        email = self.email_input.text()
        password = self.password_input.text()

        # Validate email and password
        if not email.endswith("@gmail.com"):
            QMessageBox.warning(self, "Registration Error", "Email must end with @gmail.com")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Registration Error", "Password must be at least 8 characters long")
            return

        try:
            # Insert user data into the database
            self.cursor.execute("INSERT INTO Managers(FirstName, LastName, DepartmentID, Email, Password) VALUES (?, ?, ?, ?, ?)",
                                (first_name, last_name, department, email, password))
            self.conn.commit()
            QMessageBox.information(self, "Registration", "Registration successful!")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Registration Error", "Error occurred during registration: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationPage()
    window.show()
    sys.exit(app.exec_())
