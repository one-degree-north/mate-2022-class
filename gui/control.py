from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from .button import Button

class ControlBar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-right-radius: 10px
            }
        """)

        self.parent = parent

        self.help_button = Button('gui/icons/help_icon.png', 'Help')
        self.help_button.clicked.connect(self.help)

        self.console_button = Button('gui/icons/console_icon.png', 'Console')
        self.console_button.clicked.connect(self.console)

        # self.console_window = ConsoleWindow()

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

        self.setFixedWidth(60)

    def help(self):
        pass

    def console(self):
        # self.console_window.show()
        print(self.parent.lower_frame.children(), )

        # if self.parent.console not in self.parent.lower_frame():
        #     self.parent.lower_frame.layout.insertWidget(1, self.parent.console)

        # else:
        #     self.parent.lower_frame.layout.removeWidget(self.parent.console)

        if self.parent.console.isVisible():
            self.parent.console.hide()

        else:
            self.parent.console.show()

    def reconnect(self):
        pass

    def quit(self):
        # access camera from other windows and close
        print('\033[93m\033[1mSuccessfully stopped Crimson UI\033[0m') 

        exit()