import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
from AddEmployee import AddEmployeeDialog
from PyQt5.QtCore import QFile, QTextStream, Qt
class EditEmployeeDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier Employé")
        self.employee_data = employee_data
        self.initUI()
        self.setGeometry(750, 300, 500, 250)
    def initUI(self):
        layout = QVBoxLayout()
        self.name_entry = QLineEdit()
        self.name_entry.setText(self.employee_data[2])
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.name_entry)
        self.lname_entry = QLineEdit()
        self.lname_entry.setText(self.employee_data[3])
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.lname_entry)
        self.age_entry = QLineEdit()
        self.age_entry.setText(str(self.employee_data[4]))
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age_entry)
        self.poste_combo = QComboBox()
        self.poste_combo.addItems(["Normal Employee", "Head Employee"])
        self.poste_combo.setCurrentText(self.employee_data[6])
        layout.addWidget(QLabel("Poste:"))
        layout.addWidget(self.poste_combo)
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_employee)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
    def save_employee(self):
        new_name = self.name_entry.text()
        new_lname = self.lname_entry.text()
        new_age = self.age_entry.text()
        new_poste = self.poste_combo.currentText()
        try:
            conn = sqlite3.connect('gestion_des_employes.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Employees SET FirstName=?, LastName=?, Age=?, PositionID=? WHERE ID=?",
                           (new_name, new_lname, new_age, new_poste, self.employee_data[0]))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Employee information updated successfully.")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
class ViewEmployeesWindow(QMainWindow):
    def __init__(self, department_id):
        super().__init__()
        self.setWindowTitle("Liste des Employés")
        self.setGeometry(250, 100, 1400, 900)
        self.setFocusPolicy(Qt.StrongFocus)
        self.department_id = department_id
        self.initUI()
        self.conn = sqlite3.connect('gestion_des_employes.db')
        self.cur = self.conn.cursor()
        self.populate_employee_table()
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.back_button_clicked)
        self.back_button.setStyleSheet('width: 100px; background-color: #6d6ffa;color: white; padding: 10px 20px; border: none; border-radius: 5px;')
        title_label = QLabel(f"Liste De Departement {self.department_id}", alignment=Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(9)
        self.employee_table.setHorizontalHeaderLabels(["ID", "Code", "Firs Name", "Last Name", "Age", "Daprtement", "Poste"])
        layout.addWidget(self.employee_table)
        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.clicked.connect(self.add_employee_dialog)
        layout.addWidget(self.add_employee_button)
        self.central_widget.setLayout(layout)
        self.apply_stylesheet("stylesheet.css")
        
    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())

    def populate_employee_table(self):
        self.cur.execute("SELECT * FROM Employees WHERE DepartmentID = ?", (self.department_id,))
        employees = self.cur.fetchall()
        if employees:
            self.employee_table.setRowCount(len(employees))
            for row, employee in enumerate(employees):
                for col, data in enumerate(employee):
                    item = QTableWidgetItem(str(data))
                    self.employee_table.setItem(row, col, item)
                edit_button = QPushButton("Modifier")
                edit_button.clicked.connect(lambda _, row=row: self.edit_employee(row))
                self.employee_table.setCellWidget(row, 7, edit_button)
                delete_button = QPushButton("Supprimer")
                delete_button.clicked.connect(lambda _, row=row: self.delete_employee(row))
                self.employee_table.setCellWidget(row, 8, delete_button)
                self.apply_stylesheet("stylesheet.css")
        else:
            self.employee_table.setRowCount(1)
            item = QTableWidgetItem("Aucun employé trouvé")
            item.setTextAlignment(Qt.AlignCenter)
            self.employee_table.setItem(0, 0, item)
    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())
    def edit_employee(self, row):
        employee_id = int(self.employee_table.item(row, 0).text())
        self.cur.execute("SELECT * FROM Employees WHERE ID=?", (employee_id,))
        employee_data = self.cur.fetchone()
        dialog = EditEmployeeDialog(employee_data, parent=self)
        if dialog.exec_():
            self.populate_employee_table()
    def delete_employee(self, row):
        employee_id = int(self.employee_table.item(row, 0).text())
        try:
            self.cur.execute("DELETE FROM Employees WHERE ID=?", (employee_id,))
            self.conn.commit()
            self.populate_employee_table()
            QMessageBox.information(self, "Success", "Employee deleted successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while deleting the employee: {e}")
    def add_employee_dialog(self):
        self.window = AddEmployeeDialog(department_id=self.department_id, parent=self)
        self.window.show()
    def back_button_clicked(self):
        self.hide()
def main():
    app = QApplication(sys.argv)
    department_id = 1
    window = ViewEmployeesWindow(department_id)
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
