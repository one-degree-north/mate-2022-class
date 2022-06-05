from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from ..camera import Camera

import sys

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

        # Control Pannel Frame

        self.control_frame = QWidget()
        self.control_frame.layout = QVBoxLayout()

        self.control_frame.layout.addStretch(1)
        self.control_frame.layout.addWidget(self.control)

        self.control_frame.setLayout(self.control_frame.layout)

        self.control_frame.layout.setContentsMargins(0,0,0,0)


        # Layout

        self.frame = QWidget()
        self.frame.layout = QHBoxLayout()

        self.frame.layout.addWidget(self.control_frame)
        self.frame.layout.addWidget(self.cam, 100)

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

        self.help_button = Button('gui/icons/help_icon.png', 'Help')
        self.help_button.clicked.connect(self.help)

        self.console_button = Button('gui/icons/console_icon.png', 'Console')
        self.console_button.clicked.connect(self.console)

        self.reconnect_button = Button('gui/icons/reconnect_icon.png', 'Reconnect')
        self.reconnect_button.clicked.connect(self.reconnect)

        self.quit_button = Button('gui/icons/quit_icon.png', 'Quit')
        self.quit_button.clicked.connect(self.quit)


        self.layout = QVBoxLayout()

        self.layout.addStretch()
        self.layout.addWidget(self.help_button)
        self.layout.addWidget(self.console_button)
        self.layout.addWidget(self.reconnect_button)
        self.layout.addWidget(self.quit_button)


        self.setLayout(self.layout)

        self.setFixedWidth(60)

    def help(self):
        pass

    def console(self):
        pass

    def reconnect(self):
        pass

    def quit(self):
        pass

class Button(QPushButton):
    def __init__(self, icon, tip):
        super().__init__()

        self.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet("""
            QPushButton {
                background: rgb(35, 35, 35);
                color: rgb(210, 211, 210);

                font: bold 20px;

                border-radius: 5px
            }

            QPushButton:hover {
                background: rgb(50,50,50)
            }
        """)

        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(36,36))

        self.setToolTip(tip)

if __name__ == '__main__':
    app = QApplication([])

    window = FrontCamera()
    window.show()

    sys.exit(app.exec())