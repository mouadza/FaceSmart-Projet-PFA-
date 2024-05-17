import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QDialog
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QPixmap
from EmplyeeChoice import EmployeeOptionsPage
from Login import LoginRegisterWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Manager or Employee Choice')
        self.resize(800, 400)
        self.setMinimumSize(400, 200)
        self.background_label = QLabel(self)
        pixmap = QPixmap('/image/face.png')  # Use a relative path
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(100, 50, self.width(), self.height())

        # Create a QLabel for the title
        self.title_label = QLabel('Face Smart', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('padding: 40px; background-color: #2528bb; font-size: 30px; font-weight: bold; color: white;'
                                       'border-radius: 20%; ')

        self.label = QLabel('Choose your role:', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('color: #545454; font-size: 20px;')
        self.manager_button = QPushButton('Manager', self)
        self.employee_button = QPushButton('Employee', self)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.manager_button)
        self.manager_button.clicked.connect(self.open_manager_window)
        button_layout.addWidget(self.employee_button)
        self.employee_button.clicked.connect(self.open_employee_options_dialog)
        self.manager_button.setCursor(Qt.PointingHandCursor)
        self.employee_button.setCursor(Qt.PointingHandCursor)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.label)
        layout.addStretch(1)  # Add a stretchable space
        layout.addLayout(button_layout)  # Add button layout
        layout.addStretch(1)  # Add another stretchable space
        self.setLayout(layout)

        # Center the window on the screen
        self.center()

        # Apply CSS styling
        self.apply_stylesheet("stylesheet.css")

    def center(self):
        # Function to center the window on the screen
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())

    def open_manager_window(self):
        self.manager_window = LoginRegisterWindow()
        self.manager_window.show()

    def open_employee_options_dialog(self):
        self.window = EmployeeOptionsPage()
        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
