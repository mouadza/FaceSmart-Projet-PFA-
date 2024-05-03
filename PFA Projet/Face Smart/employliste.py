import sys
import cv2
import string
import random
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QDialog,QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt

def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
class EditEmployeeDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier Employé")
        self.employee_data = employee_data
        self.initUI()
        self.setGeometry(720, 260, 400, 200)
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
        self.setGeometry(450, 150, 1000, 800)
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
        else:
            self.employee_table.setRowCount(1)
            item = QTableWidgetItem("Aucun employé trouvé")
            item.setTextAlignment(Qt.AlignCenter)
            self.employee_table.setItem(0, 0, item)
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
        dialog = AddEmployeeDialog(department_id=self.department_id, parent=self)
        if dialog.exec_():
            self.populate_employee_table()
class AddEmployeeDialog(QDialog):
    def __init__(self, department_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter Employé")
        self.department_id = department_id 
        self.initUI()
        self.setGeometry(720, 260, 400, 200)
        self.capture = cv2.VideoCapture(0) 
    def initUI(self):
        layout = QVBoxLayout()
        self.name_entry = QLineEdit()
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.name_entry)
        self.lname_entry = QLineEdit()
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.lname_entry)
        self.age_entry = QLineEdit()  
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age_entry)  
        self.poste_combo = QComboBox()  
        self.poste_combo.addItems(["Normal Employee", "Head Employee"])  
        layout.addWidget(QLabel("Poste:"))
        layout.addWidget(self.poste_combo)  
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 250)
        self.add_image_button = QPushButton("Add Image")
        self.add_image_button.clicked.connect(self.select_image)
        layout.addWidget(QLabel("Image:"))
        layout.addWidget(self.image_label)
        layout.addWidget(self.add_image_button)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_employee)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if image_path:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaledToWidth(200)  
            self.image_label.setPixmap(pixmap)
            self.image_path = image_path
    def save_employee(self):
        name = self.name_entry.text()
        lname = self.lname_entry.text()
        age = self.age_entry.text()
        poste = self.poste_combo.currentText()
        if name == "" or lname == "" or age == "" or poste == "":
            QMessageBox.warning(self, "Registration Error", "All fields must be filled out")
            return 
        if not hasattr(self, 'image_path') or not self.image_path:
            QMessageBox.warning(self, "Image Error", "Please select an image first")
            return 
        conn = sqlite3.connect('gestion_des_employes.db')
        cursor = conn.cursor()
        try:
            emp_code = generate_random_code()
            with open(self.image_path, "rb") as file:
                image_data = file.read()
            cursor.execute("INSERT INTO Employees(Code, FirstName, LastName, Age, DepartmentID, PositionID, Image) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (emp_code, name, lname, age, self.department_id, poste, image_data))
            conn.commit()
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Success", "Employee added successfully.")
                self.clear_fields()
                self.image_label.clear()
            else:
                QMessageBox.warning(self, "Error", "Failed to add employee.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        conn.close()
    def clear_fields(self):
        self.name_entry.clear()
        self.lname_entry.clear()
        self.age_entry.clear()
        self.poste_combo.setCurrentIndex(0) 
def main():
    app = QApplication(sys.argv)
    window = ViewEmployeesWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
def main():
    app = QApplication(sys.argv)
    window = ViewEmployeesWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
