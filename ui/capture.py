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

        self.capture_image_button = Button('ui/icons/capture_image_icon.png', 'Capture image')
        self.capture_image_button.clicked.connect(self.capture_image)

        self.record_button = Button('ui/icons/start_record_icon.png', 'Start recording')
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
        time = datetime.now().strftime(f"%d-%m-%y_%H:%M:%S.%f")[:-4]

        try:
            filename = f'captures/IMAGES/{time}-front_camera.png'
            cv2.imwrite(filename, self.parent.grid.front_cam.thread.image)

            logging.info(f'Image captured under: captures/IMAGES/{time}-front_camera.png')
        except cv2.error:
            logging.error('An error occurred while attempting to capture an image from the FRONT camera')
            # pass

        try:
            filename = f'captures/IMAGES/{time}-down_camera.png'
            cv2.imwrite(filename, self.parent.grid.down_cam.thread.image)


            logging.info(f'Image captured under: captures/IMAGES/{time}-down_camera.png')
        except cv2.error:
            logging.error('An error occurred while attempting to capture an image from the DOWN camera')
            # pass

    def toggle_record(self):
        if not self.recording:
            if self.parent.stopwatch_control.quickstart_button.isEnabled():
                self.parent.stopwatch_control.quickstart_button.setDisabled(True)

            self.record_button.setIcon(QIcon('ui/icons/stop_record_icon.png'))
            self.record_button.setToolTip('Stop recording')

            

            self.time = datetime.now().strftime(f"%d-%m-%y_%H:%M:%S.%f")[:-4]

            try:
                filename = f'captures/VIDEOS/{self.time}-front_video.avi'
                self.parent.grid.front_cam.thread.video_output = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (self.parent.grid.front_cam.thread.image.shape[1], self.parent.grid.front_cam.thread.image.shape[0]))
                # logging.info(f'Video captured under: captures/{folder}/front_video.mp4')
                logging.info('Started video capture from the FRONT camera')
            except AttributeError:
                logging.error('An error occurred while attempting to start video capture from the FRONT camera')

            try:
                filename = f'captures/VIDEOS/{self.time}-down_video.avi'
                self.parent.grid.down_cam.thread.video_output = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (self.parent.grid.down_cam.thread.image.shape[1], self.parent.grid.down_cam.thread.image.shape[0]))
                
                logging.info('Started video capture from the DOWN camera')
            except AttributeError:
                logging.error('An error occurred while attempting to start video capture from the DOWN camera')
            
            # from time import sleep
            # sleep(1)
            self.recording = True
            
        else:
            self.recording = False

            QTimer.singleShot(100, self.release_record)

            self.record_button.setIcon(QIcon('ui/icons/start_record_icon.png'))
            self.record_button.setToolTip('Start recording')

            self.centiseconds = 0
            self.seconds = 0
            self.minutes = 0

            self.record_stopwatch_label.setText('00:00')

            if self.parent.stopwatch.centiseconds == 0 and self.parent.stopwatch.seconds == 0 and self.parent.stopwatch.minutes == 0:
                self.parent.stopwatch_control.quickstart_button.setDisabled(False)

            # output both recordings to captures + delay?

    def release_record(self):
        # if self.parent.grid.front_cam.thread.video_output.isOpened():
        #     print('open1')
        try:
            self.parent.grid.front_cam.thread.video_output.release()
            logging.info(f'Video saved under: captures/VIDEOS/{self.time}-front_video.avi')
        except AttributeError:
            logging.error('An error occurred while attempting to save a video from the FRONT camera')
        
        try:
            self.parent.grid.down_cam.thread.video_output.release()
            logging.info(f'Video saved under: captures/VIDEOS/{self.time}-down_video.avi')
        except AttributeError:
            logging.error('An error occurred while attempting to save a video from the DOWN camera')

        # print('ok')
        # print(self.parent.grid.down_cam.thread.video_output)