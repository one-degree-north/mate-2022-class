from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from .button import Button

class ControlBar(QWidget):
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

        self.reconnect_button = Button('gui/icons/reload_icon.png', 'Reconnect')
        self.reconnect_button.clicked.connect(self.reconnect)

        self.quit_button = Button('gui/icons/quit_icon.png', 'Quit')
        self.quit_button.clicked.connect(self.quit)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.help_button)
        self.layout.addWidget(self.console_button)
        self.layout.addWidget(self.reconnect_button)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)


        # self.layout = QVBoxLayout()

        # self.layout.addStretch(1)
        # self.layout.addWidget(self.frame)

        # self.layout.setContentsMargins(0,0,0,0)
        # self.setLayout(self.layout)

        self.setFixedWidth(60)

    def help(self):
        pass

    def console(self):
        pass

    def reconnect(self):
        pass

    def quit(self):
        # access camera from other windows and close
        print('\033[93m\033[1mSuccessfully stopped Crimson UI\033[0m') 

        exit()