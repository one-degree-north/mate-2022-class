from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class ControlWidget(QWidget):
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

        # self.layout.addStretch()
        self.layout.addWidget(self.help_button)
        self.layout.addWidget(self.console_button)
        self.layout.addWidget(self.reconnect_button)
        self.layout.addWidget(self.quit_button)


        self.setLayout(self.layout)

        self.setFixedWidth(60)
        # self.help_window = HelpWindow()

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

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-left-radius: 10px
            }
        """)

        self.front_cam_status = Status('F', 'Front camera')
        self.back_cam_status = Status('D', 'Down camera')
        self.serial_status = Status('S', 'Serial connection')


        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.front_cam_status)
        self.layout.addWidget(self.back_cam_status)
        self.layout.addWidget(self.serial_status)
        
        self.setLayout(self.layout)

        self.setFixedWidth(40)

        self.front_cam_status.connected()

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-bottom-right-radius: 10px
            }
        """)
        
        self.stopwatch = QLabel('00:03:23')
        self.stopwatch.setStyleSheet("""
            QLabel {
                font: bold 30px;
                color: white
            }
        """)


        self.startstop_button = Button('gui/icons/play_icon.png', 'Start')
        self.startstop_button.clicked.connect(self.startstop)

        self.stopwatch_on = False

        self.reset_button = Button('gui/icons/reload_icon.png', 'Reset')
        self.reset_button.clicked.connect(self.reset)
        
        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.stopwatch)
        self.layout.addWidget(self.startstop_button)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

        self.setFixedHeight(60)


    def startstop(self):
        if self.stopwatch_on:
            self.stopwatch_on = False

            self.startstop_button.setIcon(QIcon('gui/icons/play_icon.png'))
            self.startstop_button.setToolTip('Resume')
            print(self.stopwatch_on)
            return
            
        

        self.startstop_button.setIcon(QIcon('gui/icons/pause_icon.png'))
        self.startstop_button.setToolTip('Pause')

        self.stopwatch_on = True

        print(self.stopwatch_on)

    def reset(self):
        self.stopwatch_on = False
        self.stopwatch.setText('00:00:00')

        self.startstop_button.setIcon(QIcon('gui/icons/play_icon.png'))
        self.startstop_button.setToolTip('Start')

class ConsolePopup(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet

class Status(QLabel):
    def __init__(self, text, tip):
        super().__init__(text)

        self.setStyleSheet("""
            QLabel {
                color: rgb(140, 26, 17);
                font: bold 25px
            }
        """)


        self.setAlignment(Qt.AlignCenter)
        self.setToolTip(tip)

    def connected(self):
        self.setStyleSheet("""
            QLabel {
                color: rgb(29, 177, 0);
                font: bold 25px
            }
        """)

    def disconnected(self):
        self.setStyleSheet("""
            QLabel {
                color: rgb(140, 26, 17);
                font: bold 25px
            }
        """)

class Button(QPushButton):
    def __init__(self, icon, tip):
        super().__init__()

        self.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet("""
            QPushButton {
                background: rgb(35, 35, 35);
                border-radius: 5px
            }

            QPushButton:hover {
                background: rgb(50,50,50)
            }
        """)

        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(40,40))

        self.setToolTip(tip)