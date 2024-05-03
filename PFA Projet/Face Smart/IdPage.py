import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialogButtonBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
from PyQt5.QtWidgets import QHBoxLayout
from TaskPage import PortfolioWidget

class EmployeeInfoDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Employee Information")
        self.resize(600, 500) 
        layout = QVBoxLayout()
        image_data = employee_data[7]
        if image_data:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignCenter) 
            image_label.setPixmap(pixmap.scaledToWidth(200,1000)) 
            layout.addWidget(image_label)
        departement_id = employee_data[5]
        info_labels = [
            f"<h3 style='color: darkgray'>First Name: <b style='color: black'>{employee_data[2]}</b></</h3>",
            f"<h3 style='color: darkgray'>Last Name: <b style='color: black'>{employee_data[3]}</b></h3>",
            f"<h3 style='color: darkgray'>Age:  <b style='color: black'>{employee_data[4]}</b></h3>",
            f"<h3 style='color: darkgray'>Departement: <b style='color: black'>Departement {departement_id}</b></h3>",
            f"<h3 style='color: darkgray'>Poste:  <b style='color: black'>{employee_data[6]}</b></h3>",
        ]
        for info in info_labels:
            label = QLabel(info)
            layout.addWidget(label)
        button_box = QDialogButtonBox()
        ok_button = button_box.addButton("Ok", QDialogButtonBox.AcceptRole)
        self.task_button = button_box.addButton("Your Task", QDialogButtonBox.ActionRole)
        ok_button.clicked.connect(self.accept)
        self.task_button.clicked.connect(self.open_task_window)
        layout.addWidget(button_box, alignment=Qt.AlignHCenter)
        self.setLayout(layout)
    def open_task_window(self):
        departement_id = self.departement_id
        code = self.code
        task_dialog = QDialog(self)
        task_dialog.setWindowTitle("Your Tasks")
        task_layout = QVBoxLayout()
        task_widget = PortfolioWidget(departement_id, code)
        task_layout.addWidget(task_widget)
        task_dialog.setLayout(task_layout)
        task_dialog.exec_()
    def set_departement_id_code(self, departement_id, code):
        self.departement_id = departement_id
        self.code = code
class ViewEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View Employee")
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()
        self.setGeometry(700, 400, 500, 200)
        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.back_button_clicked)
        title_label = QLabel(f"Enter your Code:", alignment=Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)
        self.code_entry = QLineEdit()
        self.code_entry.setPlaceholderText("Enter Employee Code")
        layout.addWidget(self.code_entry)
        self.display_button = QPushButton("Display Employee")
        self.display_button.clicked.connect(self.display_employee)
        layout.addWidget(self.display_button)
        self.setLayout(layout)
    def display_employee(self):
        code = self.code_entry.text()
        if code:
            conn = sqlite3.connect('gestion_des_employes.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Employees WHERE Code=?", (code,))
            employee_data = cursor.fetchone()
            if employee_data:
                dialog = EmployeeInfoDialog(employee_data, parent=self)
                departement_id = employee_data[5]
                dialog.set_departement_id_code(departement_id, code)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "Employee Not Found", "Employee with the provided code was not found.")
            conn.close()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a code.")
    def back_button_clicked(self):
        self.hide()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ViewEmployeeDialog()
    dialog.show()
    sys.exit(app.exec_())

