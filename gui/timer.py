from PyQt5.QtWidgets import QHBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QTimer

from .button import Button

class TimerBar(QWidget): #change to stopwatchbar
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-bottom-right-radius: 10px
            }
        """)
        
        self.stopwatch = QLabel('00:00:00')
        self.stopwatch.setStyleSheet("""
            QLabel {
                font: bold 30px;
                color: white
            }
        """)

        self.seconds = 0
        self.minutes = 0
        self.hours = 0

        self.stopwatch_on = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stopwatch)
        self.timer.start(1000)

        self.startstop_button = Button('gui/icons/play_icon.png', 'Start')
        self.startstop_button.clicked.connect(self.startstop)


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

        for _ in range(275):
            self.update_stopwatch()


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

        self.seconds = 0
        self.minutes = 0
        self.hours = 0

        self.stopwatch.setText('00:00:00')

        self.startstop_button.setIcon(QIcon('gui/icons/play_icon.png'))
        self.startstop_button.setToolTip('Start')

    def update_stopwatch(self):
        if not self.stopwatch_on:
            return

        self.total_seconds = self.seconds + (self.minutes * 60) + (self.hours * 3600) + 1

        self.minutes, self.seconds = divmod(self.total_seconds, 60)
        self.hours, self.minutes = divmod(self.minutes, 60)

        self.stopwatch.setText(f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}')