import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Choice")
        self.setGeometry(700, 400, 500, 200)
        layout = QVBoxLayout()
        self.screen_button = QPushButton("Take a Screenshot")
        self.screen_button.clicked.connect(self.take_screenshot)
        self.info_button = QPushButton("View your Info")
        self.info_button.clicked.connect(self.view_info)
        self.info_label = QLabel()
        layout.addWidget(self.screen_button)
        layout.addWidget(self.info_button)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
    def take_screenshot(self):
        self.info_label.setText("Screenshot taken")
    def view_info(self):
        self.info_label.setText("Your information goes here")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
