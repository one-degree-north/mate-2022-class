from PyQt5.QtWidgets import QHBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QTimer

from .button import Button

class CaptureControlBar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px
            }
        """)

        self.parent = parent

        self.capture_image_button = Button('gui/icons/capture_image_icon.png', 'Capture image')
        self.capture_image_button.clicked.connect(self.capture_image)

        self.record_button = Button('gui/icons/start_record_icon.png', 'Start recording')
        self.record_button.clicked.connect(self.toggle_record)

        self.recording = False

        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.capture_image_button)
        self.layout.addWidget(self.record_button)

        self.setLayout(self.layout)

    def capture_image(self):
        pass

    def toggle_record(self):
        if not self.recording:
            self.parent.stopwatch_control.startstop_button.setDisabled(True)
            self.parent.stopwatch_control.reset_button.setDisabled(True)

            self.parent.stopwatch_control.reset()

            self.record_button.setIcon(QIcon('gui/icons/stop_record_icon.png'))
            self.record_button.setToolTip('Stop recording')

            self.recording = True
            self.parent.stopwatch.stopwatch_on = True

            # record stuff or check here from grid
        else:
            self.parent.stopwatch_control.startstop_button.setDisabled(False)
            self.parent.stopwatch_control.reset_button.setDisabled(False)
            

            self.record_button.setIcon(QIcon('gui/icons/start_record_icon.png'))
            self.record_button.setToolTip('Start recording')

            self.recording = False
            print(self.parent.stopwatch.minutes, self.parent.stopwatch.seconds, self.parent.stopwatch.centiseconds)

            self.parent.stopwatch_control.reset()

            # output both recordings to captures + delay?

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


        self.startstop_button = Button('gui/icons/play_icon.png', 'Start')
        self.startstop_button.clicked.connect(self.startstop)

        self.reset_button = Button('gui/icons/reset_icon.png', 'Reset')
        self.reset_button.clicked.connect(self.reset)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.startstop_button)
        self.layout.addWidget(self.reset_button)


        self.setLayout(self.layout)

    def startstop(self):
        if self.parent.stopwatch.stopwatch_on:
            self.parent.stopwatch.stopwatch_on = False

            self.startstop_button.setIcon(QIcon('gui/icons/play_icon.png'))
            self.startstop_button.setToolTip('Resume')

            return
            

        self.startstop_button.setIcon(QIcon('gui/icons/pause_icon.png'))
        self.startstop_button.setToolTip('Pause')

        self.parent.stopwatch.stopwatch_on = True

    def reset(self):
        self.parent.stopwatch.stopwatch_on = False

        self.parent.stopwatch.milliseconds = 0
        self.parent.stopwatch.seconds = 0
        self.parent.stopwatch.minutes = 0

        self.parent.stopwatch.stopwatch_label.setText('00:00.00')

        self.startstop_button.setIcon(QIcon('gui/icons/play_icon.png'))
        self.startstop_button.setToolTip('Start')

class Stopwatch(QWidget): #change to stopwatchbar
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