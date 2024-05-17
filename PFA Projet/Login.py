import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog
from Registration import RegistrationPage
from employliste import ViewEmployeesWindow
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import QFile, QTextStream, Qt
from ManagerChoice import PopupDialog
class LoginRegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Register")
        self.setGeometry(700, 400, 500, 200)
        layout = QVBoxLayout()
        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.back_button_clicked)
        self.back_button.setStyleSheet('background-color: #6d6ffa;color: white; padding: 10px 20px; border: none; border-radius: 5px;')
        self.email_input = QLineEdit()
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        login_button = QPushButton("Login")
        register_button = QPushButton("Register")
        register_button.setStyleSheet('''
            QPushButton{
                background-color: #2248bb;
                border: 2px dotted rgb(244, 242, 242);
                color: rgb(200, 229, 252);
                padding: 15px 32px;
                border-radius: 20%;
                text-decoration: wavy;
                font-size: 16px;
                margin: 4px 2px;
                font-size: 18px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2218bb;
                border: 1px dotted rgb(4, 4, 4);
                color: white;
            }
        ''')
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)
        login_button.setCursor(Qt.PointingHandCursor)
        register_button.setCursor(Qt.PointingHandCursor)
        self.setLayout(layout)
        self.conn = sqlite3.connect('gestion_des_employes.db')
        self.cursor = self.conn.cursor()
        self.department_id = None
        self.apply_stylesheet("stylesheet.css")
        
    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        try:
            self.cursor.execute("SELECT * FROM Managers WHERE Email=? AND Password=?", (email, password))
            user = self.cursor.fetchone()
            if user:
                self.department_id = user[3]
                self.window = PopupDialog(self.department_id)  
                self.window.show()
            else:
                QMessageBox.warning(self, "Login Error", "Incorrect email or password. Please try again.")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Login Error", "Error occurred during login: " + str(e))
    def show_dialog(self, department_id):
        self.department_id = department_id
        self.show()
    def register(self):
        self.win = RegistrationPage()
        self.win.show()
    def closeEvent(self, event):
        self.conn.close()
        event.accept()
    def back_button_clicked(self):
        self.hide()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegisterWindow()
    window.show()
    sys.exit(app.exec_())
