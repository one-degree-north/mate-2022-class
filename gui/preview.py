from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

import cv2

class PreviewWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.image1 = cv2.imread('captures/front_camera.png', cv2.IMREAD_UNCHANGED)
        self.image1 = QImage(self.image1.data, self.image1.shape[1]/4, self.image1.shape[0]/4, QImage.Format_RGB888)


        self.image1_frame = QLabel()
        self.image1_frame.setPixmap(QPixmap.fromImage(self.image1))

        # self.image1_frame.setStyleSheet("""
        #     QWidget {
        #         padding: 10px
        #     }
        # """)

        self.image1_frame.setAlignment(Qt.AlignCenter)

        self.image2 = cv2.imread('captures/down_camera.png', cv2.IMREAD_UNCHANGED)
        self.image2 = QImage(self.image2.data, self.image2.shape[1]/4, self.image2.shape[0]/4, QImage.Format_RGB888)


        self.image2_frame = QLabel()
        self.image2_frame.setPixmap(QPixmap.fromImage(self.image2))

        # self.image1_frame.setStyleSheet("""
        #     QWidget {
        #         padding: 10px
        #     }
        # """)

        self.image2_frame.setAlignment(Qt.AlignCenter)

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.image1_frame)
        self.layout.addWidget(self.image2_frame)

        self.setLayout(self.layout)