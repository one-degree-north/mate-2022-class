from PyQt5.QtWidgets import QHBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

from .button import Button

class StopwatchControlBar(QWidget):
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


        self.startstop_button = Button('ui/icons/play_icon.png', 'Start')
        self.startstop_button.clicked.connect(self.startstop)

        self.reset_button = Button('ui/icons/reset_icon.png', 'Reset')
        self.reset_button.clicked.connect(self.reset)

        self.quickstart_button = Button('ui/icons/quickstart_icon.png', 'Quickstart')
        self.quickstart_button.clicked.connect(self.quickstart)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.startstop_button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.quickstart_button)


        self.setLayout(self.layout)

    def timer(self):
        print('ok')

    def quickstart(self):
        self.startstop()
        self.parent.capture_control.toggle_record()

        self.quickstart_button.setDisabled(True)

    def startstop(self):
        if self.parent.stopwatch.stopwatch_on:
            self.parent.stopwatch.stopwatch_on = False

            self.startstop_button.setIcon(QIcon('ui/icons/play_icon.png'))
            self.startstop_button.setToolTip('Resume')

        else:
            if self.quickstart_button.isEnabled():
                self.quickstart_button.setDisabled(True)

            self.startstop_button.setIcon(QIcon('ui/icons/pause_icon.png'))
            self.startstop_button.setToolTip('Pause')

            self.parent.stopwatch.stopwatch_on = True

    def reset(self):
        self.parent.stopwatch.stopwatch_on = False

        self.parent.stopwatch.centiseconds = 0
        self.parent.stopwatch.seconds = 0
        self.parent.stopwatch.minutes = 0

        self.parent.stopwatch.stopwatch_label.setText('00:00.00')

        self.startstop_button.setIcon(QIcon('ui/icons/play_icon.png'))
        self.startstop_button.setToolTip('Start')

        if not self.parent.capture_control.recording:
            self.parent.stopwatch_control.quickstart_button.setDisabled(False)

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) #needed?

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-bottom-right-radius: 10px
            }
        """)
        
        self.stopwatch_label = QLabel('00:00.00')
        self.stopwatch_label.setStyleSheet("""
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

        self.layout.addWidget(self.stopwatch_label)


        self.setLayout(self.layout)

        self.setFixedHeight(60)



    def update_stopwatch(self):
        if not self.stopwatch_on:
            return

        self.total_centiseconds = self.centiseconds + (self.seconds * 100) + (self.minutes * 6000) + 1

        self.seconds, self.centiseconds = divmod(self.total_centiseconds, 100)
        self.minutes, self.seconds = divmod(self.seconds, 60)

        self.stopwatch_label.setText(f'{self.minutes:02d}:{self.seconds:02d}.{self.centiseconds:02d}')