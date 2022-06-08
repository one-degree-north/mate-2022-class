from PyQt5.QtWidgets import QHBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from .button import Button

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


        # self.layout = QHBoxLayout()

        # self.layout.addWidget(self.frame)
        # self.layout.addStretch(1)

        # self.layout.setContentsMargins(0,0,0,0)
        # self.setLayout(self.layout)

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