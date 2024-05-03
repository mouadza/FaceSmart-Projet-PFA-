import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QTextEdit
import sqlite3

class PortfolioWidget(QWidget):
    def __init__(self, departement_id,code, parent=None):
        super().__init__()
        self.departement_id = departement_id
        self.code = code
        self.setWindowTitle('Employee Portfolio')
        self.initUI()
    def initUI(self):
        self.setGeometry(700, 400, 500, 200)
        self.project_label = QLabel('Project:')
        self.project_input = QComboBox() 
        self.task_label = QLabel('Task:')
        self.task_input = QComboBox()
        self.task_input.addItems(['Conception', 'Front-end', 'Back-end','Uses of AI'])
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_task)
        self.info_label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.project_label)
        layout.addWidget(self.project_input) 
        layout.addWidget(self.task_label)
        layout.addWidget(self.task_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
        self.populate_projects()
    def populate_projects(self):
        connection = sqlite3.connect('gestion_des_employes.db')
        cursor = connection.cursor()
        cursor.execute("SELECT  Id, ProjectName FROM Projects WHERE DepartmentID=?", (self.departement_id,))
        projects = cursor.fetchall()
        for project_id, project_name in projects:
            self.project_input.addItem(f"{project_name}")
        connection.close()
    def submit_task(self):
        project_name = self.project_input.currentText()
        selected_task = self.task_input.currentText()
        task_info = self.info_label.text() 
        connection = sqlite3.connect('gestion_des_employes.db')
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM Projects WHERE ProjectName=?", (project_name,))
        project_id_tuple = cursor.fetchone()

        if project_id_tuple:
            project_id = project_id_tuple[0]
            cursor.execute("INSERT INTO Tasks (EmployeeCode, ProjectID, TaskDescription) VALUES (?, ?, ?)",
                        (self.code, project_id, selected_task))
            connection.commit()
            connection.close()
            self.info_label.setText("Task submitted successfully.")
        else:
            connection.close()
            self.info_label.setText("Project not found.")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PortfolioWidget()
    widget.show()
    sys.exit(app.exec_())
