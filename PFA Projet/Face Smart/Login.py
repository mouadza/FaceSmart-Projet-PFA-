import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog
from Registration import RegistrationPage
from employliste import ViewEmployeesWindow
from TasksInfo import PortfolioWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel

class CreateProjectDialog(QDialog):
    def __init__(self, department_id, parent=None):
        super().__init__(parent)
        self.department_id = department_id
        self.setWindowTitle("Create Project")
        self.setGeometry(800, 450, 300, 150)
        layout = QVBoxLayout()
        self.project_name_input = QLineEdit()
        layout.addWidget(QLabel("Project Name:"))
        layout.addWidget(self.project_name_input)
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_project)
        layout.addWidget(self.create_button)
        self.setLayout(layout)
    def create_project(self):
        project_name = self.project_name_input.text()
        if project_name:
            try:
                conn = sqlite3.connect('gestion_des_employes.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Projects (ProjectName, DepartmentID) VALUES (?, ?)", (project_name, self.department_id))
                conn.commit()
                conn.close()
                self.accept()
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Database Error", "Error occurred during database operation: " + str(e))
        else:
            QMessageBox.warning(self, "Error", "Please enter a project name.")
class PopupDialog(QDialog):
    def __init__(self, department_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manager roles")
        self.setGeometry(800, 450, 300, 200)
        layout = QVBoxLayout()
        self.view_employees_button = QPushButton("View Employees")
        self.view_tasks_button = QPushButton("View Tasks")
        self.create_project_button = QPushButton("Create Project")
        layout.addWidget(self.view_employees_button)
        layout.addWidget(self.view_tasks_button)
        layout.addWidget(self.create_project_button)
        self.setLayout(layout)
        self.create_project_button.clicked.connect(parent.create_project)
class LoginRegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Register")
        self.setGeometry(700, 400, 500, 200)
        layout = QVBoxLayout()
        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.back_button_clicked)
        self.email_input = QLineEdit()
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        login_button = QPushButton("Login")
        register_button = QPushButton("Register")
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)
        self.setLayout(layout)
        self.conn = sqlite3.connect('gestion_des_employes.db')
        self.cursor = self.conn.cursor()
        self.department_id = None
    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        try:
            self.cursor.execute("SELECT * FROM Managers WHERE Email=? AND Password=?", (email, password))
            user = self.cursor.fetchone()
            if user:
                self.department_id = user[3] 
                popup = PopupDialog(self.department_id, self)  
                popup.view_employees_button.clicked.connect(lambda: self.show_view_employees(self.department_id))
                popup.exec_()
            else:
                QMessageBox.warning(self, "Login Error", "Incorrect email or password. Please try again.")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Login Error", "Error occurred during login: " + str(e))
    def show_view_employees(self, department_id):
        self.win = ViewEmployeesWindow(department_id)
        self.win.show()
        self.win.raise_()
        self.win.activateWindow()   
    def create_project(self):
        if self.department_id is not None:
            dialog = CreateProjectDialog(self.department_id, self)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Error", "Please log in first.")
    def register(self):
        self.win = RegistrationPage()
        self.win.show()
    def view_task(self):
        self.win = PortfolioWidget()
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
