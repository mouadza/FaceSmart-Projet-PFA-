import sys
import cv2
import string
import random
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QDialog,QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
import face_recognition
import json

def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
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

            # Compute face encoding
            image = face_recognition.load_image_file(self.image_path)
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) == 0:
                QMessageBox.warning(self, "Face Detection Error", "No face detected in the image.")
                return
            face_encoding = face_encodings[0]  # Assuming there's only one face in the image

            # Convert face encoding to JSON string
            face_encoding_json = json.dumps(face_encoding.tolist())

            # Insert employee data into the database
            cursor.execute(
                "INSERT INTO Employees(Code, FirstName, LastName, Age, DepartmentID, PositionID, Image, face_encoding) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (emp_code, name, lname, age, self.department_id, poste, image_data, face_encoding_json))

            conn.commit()
            known_encodings = []
            known_codes = []
            if cursor.rowcount > 0:
                # Compute the face encodings again and add them to the known encodings list
                new_face_encodings = face_recognition.face_encodings(image)
                if len(new_face_encodings) > 0:
                    known_encodings.append(new_face_encodings[0])
                    known_codes.append(emp_code)
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
    window = AddEmployeeDialog()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()