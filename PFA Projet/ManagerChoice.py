import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog
from Registration import RegistrationPage
from employliste import ViewEmployeesWindow
from PyQt5.QtCore import QFile, QTextStream, Qt
from TasksInfo import PortfolioWidget2


class CreateProjectDialog(QDialog):
    def __init__(self, department_id, parent=None):
        super().__init__(parent)
        self.department_id = department_id
        self.setWindowTitle("Create Project")
        self.setGeometry(700, 500, 500, 200)
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
                cursor.execute("INSERT INTO Projects (ProjectName, DepartmentID) VALUES (?, ?)",
                               (project_name, self.department_id))
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
        self.setGeometry(700, 500, 500, 200)
        self.department_id = department_id
        layout = QVBoxLayout()
        self.view_employees_button = QPushButton("View Employees")
        self.view_tasks_button = QPushButton("View Tasks")
        self.create_project_button = QPushButton("Create Project")
        layout.addWidget(self.view_employees_button)
        layout.addWidget(self.view_tasks_button)
        layout.addWidget(self.create_project_button)
        self.setLayout(layout)
        self.view_employees_button.clicked.connect(self.show_view_employees)
        self.create_project_button.clicked.connect(self.create_project)
        self.view_tasks_button.clicked.connect(self.view_task)
        self.apply_stylesheet("stylesheet.css")
        
    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())

    def show_view_employees(self):
        self.win = ViewEmployeesWindow(self.department_id)
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
        self.win = PortfolioWidget2(self.department_id)
        self.win.show()

    def back_button_clicked(self):
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PopupDialog()
    window.show()
    sys.exit(app.exec_())
