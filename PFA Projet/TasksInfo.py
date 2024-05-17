import sys
from PyQt5.QtWidgets import (QLabel, QComboBox, QApplication, QWidget, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox,
                             QInputDialog, QDialog, QHBoxLayout)
from PyQt5.QtCore import QFile, QTextStream, Qt
import sqlite3

class EditEmployeeDialog(QDialog):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier Status")
        self.task_data = task_data
        self.initUI()
        self.setGeometry(650, 260, 520, 200)
    def initUI(self):
        layout = QVBoxLayout()
        self.poste_combo = QComboBox()
        self.poste_combo.addItems(['In Progress', 'Completed', 'On Hold', 'Cancelled'])
        self.poste_combo.setCurrentText(self.task_data[4])
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_employee)
        layout.addWidget(self.poste_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.apply_stylesheet("stylesheet.css")
    def save_employee(self):
        new_task = self.poste_combo.currentText()
        try:
            conn = sqlite3.connect('gestion_des_employes.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Tasks SET Status = ? WHERE ID = ?",
                           (new_task,self.task_data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Employee information updated successfully.")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())
class EditStatusDialog(QDialog):
    def __init__(self, current_status, choices, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Status')
        layout = QVBoxLayout()
        self.comboBox = QComboBox()
        self.comboBox.addItems(choices)
        self.comboBox.setCurrentText(current_status)
        layout.addWidget(self.comboBox)
        buttonBox = QDialog.ButtonBox(QDialog.ButtonBox.Ok | QDialog.ButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def selected_status(self):
        return self.comboBox.currentText()

class PortfolioWidget2(QWidget):
    def __init__(self, departement_id):
        super().__init__()
        self.setWindowTitle('Employee Tasks')
        self.departement_id = departement_id
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 150, 1200, 800)
        self.back_button = QPushButton("Back")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.back_button_clicked)
        self.back_button.setStyleSheet('width: 100px; background-color: #6d6ffa;color: white; padding: 10px 20px; border: none; border-radius: 5px;')
        department_label = QLabel(f"Project of Department {self.departement_id}")
        self.project_label = QLabel('Project:')
        self.project_input = QComboBox()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.load_data)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["TaskID", "Employee Name", "Project Name", "Task", "Status", "Action", "Action"])

        # Load data into the table
        self.load_data()

        # Create main layout and add widgets
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.back_button)
        main_layout.addWidget(department_label)
        main_layout.addWidget(self.project_input)
        main_layout.addWidget(self.search_button)
        main_layout.addWidget(self.table)

        # Set main layout
        self.setLayout(main_layout)
        self.populate_projects()
        self.apply_stylesheet("stylesheet.css")
        
    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())
    def populate_projects(self):
        connection = sqlite3.connect('gestion_des_employes.db')
        cursor = connection.cursor()
        cursor.execute("SELECT  Id, ProjectName FROM Projects WHERE DepartmentID=?", (self.departement_id,))
        projects = cursor.fetchall()
        for project_id, project_name in projects:
            self.project_input.addItem(f"{project_name}")
        connection.close()

    def load_data(self):
        project_name = self.project_input.currentText()
        connection = sqlite3.connect('gestion_des_employes.db')
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM Projects WHERE ProjectName=? AND DepartmentID = ?", (project_name,self.departement_id))
        project_id = cursor.fetchone()
        try:
            connection = sqlite3.connect('gestion_des_employes.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Tasks WHERE ProjectID = ?",(project_id[0],))
            data = cursor.fetchall()
            connection.close()
            self.table.setRowCount(len(data))
            for row, row_data in enumerate(data):
                print(row_data[0])
                code = row_data[1]
                ID = row_data[2]
                connection = sqlite3.connect('gestion_des_employes.db')
                cursor = connection.cursor()
                cursor.execute("SELECT FirstName, LastName FROM Employees WHERE Code=?", (code,))
                employee_name = cursor.fetchone()
                connection.close()
                conn = sqlite3.connect('gestion_des_employes.db')
                cursor = conn.cursor()
                cursor.execute("SELECT ProjectName FROM Projects WHERE ID=?", (ID,))
                project_name = cursor.fetchone()
                full_name = " ".join(employee_name) if employee_name else "Unknown"
                project_name = project_name[0] if project_name else "Unknown"
                self.table.setItem(row, 0, QTableWidgetItem(str(row_data[0])))
                self.table.setItem(row, 1, QTableWidgetItem(full_name))
                self.table.setItem(row, 2, QTableWidgetItem(project_name))
                self.table.setItem(row, 3, QTableWidgetItem(row_data[3]))
                self.table.setItem(row, 4, QTableWidgetItem(row_data[4]))
                edit_button = QPushButton("Edit Status")
                edit_button.clicked.connect(lambda _, row=row: self.edit_employee(row))
                self.table.setCellWidget(row, 5, edit_button)
                delete_button = QPushButton("Cancel")
                delete_button.clicked.connect(lambda _, row=row: self.delete_task(row))
                self.table.setCellWidget(row, 6, delete_button)
        except Exception as e:
            print("Error:", e)
    def edit_employee(self, row):
        task_id = int(self.table.item(row, 0).text())
        connection = sqlite3.connect('gestion_des_employes.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Tasks WHERE ID=?", (task_id,))
        task_data = cursor.fetchone()
        connection.close()
        dialog = EditEmployeeDialog(task_data, parent=self)
        if dialog.exec_():
            self.load_data()
    def delete_task(self, row):
        task_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete task {task_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                connection = sqlite3.connect('gestion_des_employes.db')
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Tasks WHERE ID=?", (task_id,))
                connection.commit()
                connection.close()
                self.load_data() 
            except Exception as e:
                print("Error deleting task:", e)

    def back_button_clicked(self):
        self.hide()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PortfolioWidget2()
    widget.show()
    sys.exit(app.exec_())
