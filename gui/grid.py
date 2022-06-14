from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent

from numpy import ndarray

import cv2
import logging

class Grid(QWidget):
    def __init__(self, port1, port2):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)

        self.display_width = 320
        self.display_height = 240


        self.front_cam = self.Camera(self, port1)
        self.down_cam = self.Camera(self, port2)

        self.layout.addWidget(self.front_cam)
        self.layout.addWidget(self.down_cam)

        self.setLayout(self.layout)

        self.resizeEvent = self.camera_resize

    def camera_resize(self, resizeEvent: QResizeEvent):
        self.display_width, self.display_height = (self.front_cam.width() + self.down_cam.width())/2, (self.front_cam.height() + self.down_cam.height())/2


    class Camera(QWidget):
        def __init__(self, parent, port):
            super().__init__()

            self.parent = parent

            self.camera = QLabel('Connecting...')
            self.camera.setGeometry(0, 0, self.parent.display_width, self.parent.display_height)
            self.camera.resize(self.parent.display_width, self.parent.display_height)

            self.camera.setStyleSheet("""
                QLabel {
                    font: bold 20px;
                    color: white
                }
            """)

            self.camera.setAlignment(Qt.AlignCenter)


            self.camera.setMinimumWidth(self.parent.display_width)
            self.camera.setMinimumHeight(self.parent.display_height)

            self.connected = False

            self.layout = QVBoxLayout()

            self.layout.addWidget(self.camera)

            self.setLayout(self.layout)

            self.thread = VideoThread(self, port)
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()


        def close_event(self, event):
            self.thread.stop()
            event.accept()

        @pyqtSlot(ndarray)
        def update_image(self, cv_img):
            qt_img = self.convert_cv_qt(cv_img)
            self.camera.setPixmap(qt_img)

        def convert_cv_qt(self, cv_img):
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(self.parent.display_width, self.parent.display_height, Qt.KeepAspectRatio)
            return QPixmap.fromImage(p)

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(ndarray)

    def __init__(self, parent, port):
        super().__init__()
        self.parent = parent

        self.running = True
        self.port = port

    def run(self):
        cap = cv2.VideoCapture(self.port)

        while self.running:
            ret, self.image = cap.read()

            if ret:
                self.parent.connected = True
                self.change_pixmap_signal.emit(self.image)
            else:
                self.parent.connected = False

        cap.release()

    def stop(self):
        self.running = False
        self.wait()