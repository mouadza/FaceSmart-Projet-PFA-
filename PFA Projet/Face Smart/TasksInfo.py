import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox
import sqlite3

class PortfolioWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Employee Portfolio')
        self.initUI()
    def initUI(self):
        self.setGeometry(450, 150, 1000, 800)
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["Employee Name", "Project Name", "Task", "Status", "", ""])
        self.load_data()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
    def load_data(self):
        try:
            connection = sqlite3.connect('gestion_des_employes.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Tasks")
            data = cursor.fetchall()
            connection.close()
            self.table.setRowCount(len(data))
            for row, row_data in enumerate(data):
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
                self.table.setItem(row, 0, QTableWidgetItem(full_name))
                self.table.setItem(row, 1, QTableWidgetItem(project_name))
                self.table.setItem(row, 2, QTableWidgetItem(row_data[3]))  
                self.table.setItem(row, 3, QTableWidgetItem(row_data[4]))  
                edit_status_button = QPushButton("Edit Status")
                edit_status_button.clicked.connect(lambda _, r=row: self.edit_status(r))
                self.table.setCellWidget(row, 4, edit_status_button)
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, r=row: self.delete_task(row_data[0]))
                self.table.setCellWidget(row, 5, delete_button)
        except Exception as e:
            print("Error:", e)
    def edit_status(self, row):
        current_status = self.table.item(row, 3).text()
        new_status, ok_pressed = QMessageBox.getText(self, "Edit Status", f"Enter new status for task {row + 1}:", QMessageBox.Normal, current_status)
        if ok_pressed:
            self.table.item(row, 3).setText(new_status)
            try:
                connection = sqlite3.connect('gestion_des_employes.db')
                cursor = connection.cursor()
                cursor.execute("UPDATE Tasks SET Status=? WHERE TaskID=?", (new_status, row + 1))
                connection.commit()
                connection.close()
            except Exception as e:
                print("Error updating status:", e)
    def delete_task(self, task_id):
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete task {task_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                connection = sqlite3.connect('gestion_des_employes.db')
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Tasks WHERE TaskID=?", (task_id,))
                connection.commit()
                connection.close()
                self.load_data() 
            except Exception as e:
                print("Error deleting task:", e)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PortfolioWidget()
    widget.show()
    sys.exit(app.exec_())
