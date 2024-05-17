import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QDialog
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QPixmap
from IdPage import ViewEmployeeDialog
from TakeScreen import CaptureWindow
import cv2
import face_recognition
import numpy as np
import json
from face_recognition import face_distance
import sqlite3
from faceRecognition import reconnaissance_facial

class EmployeeOptionsPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Employee Options')
        self.initUI()

    def initUI(self):
        self.resize(600, 300)  # Initial size
        self.setMinimumSize(300, 150) 
        layout = QVBoxLayout()
        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setStyleSheet('background-color: #6d6ffa;color: white; padding: 10px 20px; border: none; border-radius: 5px;')
        self.back_button.clicked.connect(self.back_button_clicked)
        view_info_button = QPushButton('View Info', self)
        view_info_button.clicked.connect(self.view_info_clicked)
        take_screen_button = QPushButton('Take Screen', self)
        take_screen_button.clicked.connect(self.take_screen_clicked)
        Travel_hour = QPushButton('Face Recognition', self)
        Travel_hour.clicked.connect(self.travel_hours_clicked)
        view_info_button.setCursor(Qt.PointingHandCursor)
        take_screen_button.setCursor(Qt.PointingHandCursor)
        Travel_hour.setCursor(Qt.PointingHandCursor)
        layout.addWidget(view_info_button)
        layout.addWidget(take_screen_button)
        layout.addWidget(Travel_hour)
        

        self.setLayout(layout)
        self.apply_stylesheet("stylesheet.css")
    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())

    def view_info_clicked(self):
        self.window_manager = ViewEmployeeDialog()
        self.window_manager.show() 

    def take_screen_clicked(self):
        self.window = CaptureWindow()
        self.window.show() 
    def travel_hours_clicked(self):
        self.window = reconnaissance_facial()
        self.window.show()

    def back_button_clicked(self):
        self.hide()
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Example usage:
    # Open the Employee Options Page
    employee_options_page = EmployeeOptionsPage()
    employee_options_page.show()

    sys.exit(app.exec_())
