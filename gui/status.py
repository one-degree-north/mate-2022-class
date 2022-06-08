from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt


class StatusBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-left-radius: 10px
            }
        """)

        self.front_cam_status = Status('F', 'Front camera')
        self.back_cam_status = Status('D', 'Down camera')
        self.serial_status = Status('S', 'Serial connection')

        self.frame = QWidget()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.front_cam_status)
        self.layout.addWidget(self.back_cam_status)
        self.layout.addWidget(self.serial_status)
        
        self.setLayout(self.layout)


        # self.layout = QVBoxLayout()
        
        # self.layout.addStretch(1)
        # self.layout.addWidget(self.frame)

        # self.layout.setContentsMargins(0,0,0,0)
        # self.setLayout(self.layout)

        self.setFixedWidth(40)

        self.front_cam_status.connected()

class Status(QLabel):
    def __init__(self, text, tip):
        super().__init__(text)

        self.setStyleSheet("""
            QLabel {
                color: rgb(140, 26, 17);
                font: bold 25px
            }
        """)


        self.setAlignment(Qt.AlignCenter)
        self.setToolTip(tip)

    def connected(self):
        self.setStyleSheet("""
            QLabel {
                color: rgb(29, 177, 0);
                font: bold 25px
            }
        """)

    def disconnected(self):
        self.setStyleSheet("""
            QLabel {
                color: rgb(140, 26, 17);
                font: bold 25px
            }
        """)