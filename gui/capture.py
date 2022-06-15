from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

from .button import Button

import os

import logging
import cv2

from datetime import datetime

class CaptureControlBar(QWidget):
    def __init__(self, parent): #"parent" needed?
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

        self.record_stopwatch_label = QLabel('00:00')
        self.record_stopwatch_label.setStyleSheet("""
            QLabel {
                font: bold 20px;
                color: white
            }
        """)

        self.centiseconds = 0
        self.seconds = 0
        self.minutes = 0

        self.recording = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stopwatch)
        self.timer.start(10)

        self.capture_image_button = Button('gui/icons/capture_image_icon.png', 'Capture image')
        self.capture_image_button.clicked.connect(self.capture_image)

        self.record_button = Button('gui/icons/start_record_icon.png', 'Start recording')
        self.record_button.clicked.connect(self.toggle_record)


        self.layout = QHBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.record_stopwatch_label)
        self.layout.addWidget(self.capture_image_button)
        self.layout.addWidget(self.record_button)

        self.setLayout(self.layout)

    def update_stopwatch(self):
        if not self.recording:
            return

        self.total_centiseconds = self.centiseconds + (self.seconds * 100) + (self.minutes * 6000) + 1

        self.seconds, self.centiseconds = divmod(self.total_centiseconds, 100)
        self.minutes, self.seconds = divmod(self.seconds, 60)

        self.record_stopwatch_label.setText(f'{self.minutes:02d}:{self.seconds:02d}')

    def capture_image(self):
        folder = f'IMAGE_{datetime.now().strftime(f"%d-%m-%y_%H:%M:%S.%f")[:-4]}'
        os.mkdir(f'captures/{folder}')

        try:
            filename = f'captures/{folder}/front_camera.png'
            cv2.imwrite(filename, self.parent.grid.front_cam.thread.image)

            logging.info(f'Captured: captures/{folder}/front_camera.png')
        except cv2.error:
            logging.error('An error occurred while attempting to capture an image from the FRONT camera')
            # pass

        try:
            filename = f'captures/{folder}/down_camera.png'
            cv2.imwrite(filename, self.parent.grid.down_cam.thread.image)


            logging.info(f'Captured: captures/{folder}/down_camera.png')
        except cv2.error:
            logging.error('An error occurred while attempting to capture an image from the DOWN camera')
            # pass

    def toggle_record(self):
        if not self.recording:
            if self.parent.stopwatch_control.quickstart_button.isEnabled():
                self.parent.stopwatch_control.quickstart_button.setDisabled(True)

            self.record_button.setIcon(QIcon('gui/icons/stop_record_icon.png'))
            self.record_button.setToolTip('Stop recording')

            self.recording = True

        else:
            self.record_button.setIcon(QIcon('gui/icons/start_record_icon.png'))
            self.record_button.setToolTip('Start recording')

            self.recording = False

            self.centiseconds = 0
            self.seconds = 0
            self.minutes = 0

            self.record_stopwatch_label.setText('00:00')

            if not self.parent.stopwatch.stopwatch_on:
                self.parent.stopwatch_control.quickstart_button.setDisabled(False)

            # output both recordings to captures + delay?