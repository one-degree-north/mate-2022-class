from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QTextCursor, QResizeEvent

from numpy import ndarray

import cv2
import logging

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(ndarray)

    def __init__(self, parent, port):
        super().__init__()
        self.running = True
        self.parent = parent
        self.port = port

    def run(self):
        self.capture = cv2.VideoCapture(self.port)
        self.count = 0

        while self.running:
            ret, self.parent.image = self.capture.read()

            if ret:
                self.change_pixmap_signal.emit(self.parent.image)

        self.capture.release()

    def stop(self):
        self.running = False
        self.wait()


class Camera(QWidget):
    def __init__(self, port):
        super().__init__()

        self.display_width = 320
        self.display_height = 240


        self.camera = QLabel()
        self.camera.setGeometry(0, 0, 320, 240)
        self.camera.resize(self.display_width, self.display_height)

        self.camera.setMinimumWidth(320)
        self.camera.setMinimumHeight(240)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.camera)

        self.setLayout(self.layout)

        self.camera.resizeEvent = self.camera_resize

        self.image = None

        self.thread = VideoThread(self, port)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def camera_resize(self, resizeEvent: QResizeEvent):
        self.display_width, self.display_height = self.camera.width(), self.camera.height()

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
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)