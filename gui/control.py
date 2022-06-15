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

        self.info_button = Button('gui/icons/inputs_icon.png', 'Info')
        self.info_button.clicked.connect(self.info)

        self.console_button = Button('gui/icons/console_icon.png', 'Console')
        self.console_button.clicked.connect(self.console)

        # self.console_window = ConsoleWindow()

        self.quit_button = Button('gui/icons/quit_icon.png', 'Quit')
        self.quit_button.clicked.connect(self.quit)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.help_button)
        self.layout.addWidget(self.info_button)
        self.layout.addWidget(self.console_button)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

        self.setFixedWidth(60)

    def help(self):
        self.help_button.setDisabled(True)

    def info(self):
        if self.parent.thruster_display.isVisible():
            self.parent.thruster_display.hide()
            self.parent.axis_display.hide()
        else:
            self.parent.thruster_display.show()
            self.parent.axis_display.show()


    def console(self):
        if self.parent.console.isVisible():
            self.parent.console.hide()
        else:
            self.parent.console.show()

    def quit(self):
        # access camera from other windows and close
        print('\033[93m\033[1mSuccessfully stopped Crimson UI\033[0m') 

        exit()