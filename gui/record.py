from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

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

        self.record_stopwatch = QLabel('00:00')
        self.record_stopwatch.setStyleSheet("""
            QLabel {
                font: bold 20px;
                color: white
            }
        """)

        self.seconds = 0
        self.minutes = 0

        self.recording = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stopwatch)
        self.timer.start(1000)

        self.capture_image_button = Button('gui/icons/capture_image_icon.png', 'Capture image')
        self.capture_image_button.clicked.connect(self.capture_image)

        self.record_button = Button('gui/icons/start_record_icon.png', 'Start recording')
        self.record_button.clicked.connect(self.toggle_record)


        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.record_stopwatch)
        self.layout.addWidget(self.capture_image_button)
        self.layout.addWidget(self.record_button)

        self.setLayout(self.layout)

    def update_stopwatch(self):
        if not self.recording:
            return

        self.total_seconds = self.seconds + (self.minutes * 60) + 1
        self.minutes, self.seconds = divmod(self.total_seconds, 60)

        self.record_stopwatch.setText(f'{self.minutes:02d}:{self.seconds:02d}')

    def capture_image(self):
        pass

    def toggle_record(self):
        if not self.recording:
            self.record_button.setIcon(QIcon('gui/icons/stop_record_icon.png'))
            self.record_button.setToolTip('Stop recording')

            self.recording = True

        else:
            self.record_button.setIcon(QIcon('gui/icons/start_record_icon.png'))
            self.record_button.setToolTip('Start recording')

            self.recording = False

            self.seconds = 0
            self.minutes = 0

            self.record_stopwatch.setText('00:00')

            # output both recordings to captures + delay?