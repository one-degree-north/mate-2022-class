from PyQt5.QtWidgets import QHBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QTimer

from .button import Button

class TimerBar(QWidget): #change to stopwatchbar
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) #needed?

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-bottom-right-radius: 10px
            }
        """)
        
        self.stopwatch = QLabel('00:00.00')
        self.stopwatch.setStyleSheet("""
            QLabel {
                font: bold 30px;
                color: white
            }
        """)

        self.centiseconds = 0
        self.seconds = 0
        self.minutes = 0

        self.stopwatch_on = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stopwatch)
        self.timer.start(10)


        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.stopwatch)


        self.setLayout(self.layout)

        self.setFixedHeight(60)



    def update_stopwatch(self):
        if not self.stopwatch_on:
            return

        self.total_centiseconds = self.centiseconds + (self.seconds * 100) + (self.minutes * 6000) + 1

        self.seconds, self.centiseconds = divmod(self.total_centiseconds, 100)
        self.minutes, self.seconds = divmod(self.seconds, 60)

        self.stopwatch.setText(f'{self.minutes:02d}:{self.seconds:02d}.{self.centiseconds:02d}')

class TimerControlBar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-bottom-left-radius: 10px
            }
        """)

        self.parent = parent

        self.startstop_button = Button('gui/icons/play_icon.png', 'Start')
        self.startstop_button.clicked.connect(self.startstop)


        self.reset_button = Button('gui/icons/reload_icon.png', 'Reset')
        self.reset_button.clicked.connect(self.reset)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.startstop_button)
        self.layout.addWidget(self.reset_button)


        self.setLayout(self.layout)

    def startstop(self):
        if self.parent.timer.stopwatch_on:
            self.parent.timer.stopwatch_on = False

            self.startstop_button.setIcon(QIcon('gui/icons/play_icon.png'))
            self.startstop_button.setToolTip('Resume')

            return
            

        self.startstop_button.setIcon(QIcon('gui/icons/pause_icon.png'))
        self.startstop_button.setToolTip('Pause')

        self.parent.timer.stopwatch_on = True

    def reset(self):
        self.parent.timer.stopwatch_on = False

        self.parent.timer.milliseconds = 0
        self.parent.timer.seconds = 0
        self.parent.timer.minutes = 0

        self.parent.timer.stopwatch.setText('00:00.00')

        self.startstop_button.setIcon(QIcon('gui/icons/play_icon.png'))
        self.startstop_button.setToolTip('Start')