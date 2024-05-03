import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMainWindow
from IdPage import ViewEmployeeDialog 
from Login import LoginRegisterWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Manager or Employee Choice')
        self.setGeometry(700, 400, 500, 200)
        self.label = QLabel('Choose your role:', self)
        self.manager_button = QPushButton('Manager', self)
        self.manager_button.clicked.connect(self.open_manager_window)
        self.employee_button = QPushButton('Employee', self)
        self.employee_button.clicked.connect(self.open_employee_window)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.manager_button)
        layout.addWidget(self.employee_button)
        self.setLayout(layout)
    def open_manager_window(self):
        self.manager_window = LoginRegisterWindow()
        self.manager_window.show()
    def open_employee_window(self):
        self.manager_window = ViewEmployeeDialog()
        self.manager_window.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
