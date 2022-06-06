from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from ..camera import Camera

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QMainWindow {
                background: rgb(21, 21, 21)
            }
        """)

        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setFixedSize(300,200) -- use qtimer/wait for all cameras



        self.cam = Camera(1)

        self.control = MenuBar()
        self.timer = TimerBar()

        # Control Pannel Frame - make better

        self.control_frame = QWidget()
        self.control_frame.layout = QVBoxLayout()

        self.control_frame.layout.addStretch(1)
        self.control_frame.layout.addWidget(self.control)
        

        self.control_frame.setLayout(self.control_frame.layout)

        self.control_frame.layout.setContentsMargins(0,0,0,0)

        # Timer Frame - make better

        self.timer_frame = QWidget()
        self.timer_frame.layout = QHBoxLayout()

        self.timer_frame.layout.addWidget(self.timer)
        self.timer_frame.layout.addStretch(1)

        self.timer_frame.setLayout(self.timer_frame.layout)
        self.timer_frame.layout.setContentsMargins(0,0,0,0)

        # Layout

        self.frame = QWidget()
        self.frame.layout = QHBoxLayout()

        self.frame.layout.addWidget(self.control_frame)
        self.frame.layout.addWidget(self.cam, 100)

        self.frame.layout.setContentsMargins(0,0,0,0)
        self.frame.setLayout(self.frame.layout)

        # Main

        self.main_frame = QWidget()
        self.main_frame.layout = QVBoxLayout()
        
        self.main_frame.layout.addWidget(self.timer_frame)
        self.main_frame.layout.addWidget(self.frame, 100)

        self.main_frame.layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.main_frame.layout)

        self.setCentralWidget(self.main_frame)

        # self.frame = QWidget()
        # self.frame.layout = QGridLayout()

        # self.frame.layout.addWidget(self.timer_frame, 0,0)
        # self.frame.layout.addWidget(self.control_frame, 1,0)
        # self.frame.layout.addWidget(self.cam, 1,1,100,100)
        
        # self.frame.setContentsMargins(0,0,0,0)
        # self.frame.setLayout(self.frame.layout)


        # self.setCentralWidget(self.frame)


class MenuBar(QWidget):
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
        self.help_window = HelpWindow()

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

class TimerBar(QWidget):
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
        self.setIconSize(QSize(40,40))

        self.setToolTip(tip)

if __name__ == '__main__':
    app = QApplication([])

    window = FrontCamera()
    window.show()

    sys.exit(app.exec())