from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt

from camera import Camera

class FrontCamera(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QMainWindow {
                background: rgb(21, 21, 21)
            }
        """)

        self.cam = Camera(1)
        self.control = ControlPannel()


        self.frame = QWidget()
        self.frame.layout = QHBoxLayout()


        self.frame.layout.addWidget(self.control)
        self.frame.layout.addWidget(self.cam)

        self.frame.layout.setContentsMargins(0,0,0,0)
        self.frame.setLayout(self.frame.layout)

        self.setCentralWidget(self.frame)


class ControlPannel(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-right-radius: 10px
            }
        """)

        self.button_a = Button('A')
        self.button_b = Button('B')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button_a)
        self.layout.addWidget(self.button_b)

        print(self.button_a.width())


        self.setLayout(self.layout)

        self.setFixedWidth(80)

class Button(QPushButton):
    def __init__(self, temp_text):
        super().__init__(temp_text)

        self.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(25, 38, 62), stop:1 rgb(26, 45, 69)
                );
                color: rgb(210, 211, 210);

                font: bold 20px;

                border-radius: 5px
            }

            QPushButton:hover {
                background: rgb(45, 58, 82)
            }
        """)