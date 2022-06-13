from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer

from gui.grid import Grid
from gui.control import ControlBar
from gui.status import StatusBar
from gui.timer import TimerBar, TimerControlBar
from gui.console import ConsoleModule

import sys
import os

import yaml
import cv2

from datetime import datetime

class CrimsonUI(QMainWindow):
    def __init__(self, front_port, down_port):
        super().__init__()

        self.setStyleSheet("""
            QMainWindow {
                background: rgb(21, 21, 21)
            }
        """)

        self.grid = Grid(front_port, down_port)
        self.control = ControlBar()
        self.status = StatusBar()
        self.timer = TimerBar()
        self.timer_control = TimerControlBar(self)

        self.console = ConsoleModule()


        self.control_frame = QWidget()
        self.control_frame.layout = QVBoxLayout()
        
        self.control_frame.layout.addStretch(1)
        self.control_frame.layout.addWidget(self.control)

        self.control_frame.layout.setContentsMargins(0,0,0,0)
        self.control_frame.setLayout(self.control_frame.layout)


        self.console_frame = QWidget()
        self.console_frame.layout = QVBoxLayout()
        
        self.console_frame.layout.addStretch(1)
        self.console_frame.layout.addWidget(self.console)

        self.console_frame.layout.setContentsMargins(0,0,0,0)
        self.console_frame.setLayout(self.console_frame.layout)


        self.status_frame = QWidget()
        self.status_frame.layout = QVBoxLayout()
        
        self.status_frame.layout.addStretch(1)
        self.status_frame.layout.addWidget(self.status)

        self.status_frame.layout.setContentsMargins(0,0,0,0)
        self.status_frame.setLayout(self.status_frame.layout)


        self.timer_frame = QWidget()
        self.timer_frame.layout = QHBoxLayout()
        
        self.timer_frame.layout.addWidget(self.timer)
        self.timer_frame.layout.addStretch(1)
        self.timer_frame.layout.addWidget(self.timer_control)

        self.timer_frame.layout.setContentsMargins(0,0,0,0)
        self.timer_frame.setLayout(self.timer_frame.layout)


        self.lower_frame = QWidget()
        self.lower_frame.layout = QHBoxLayout()
        self.lower_frame.layout.setSpacing(10)

        self.lower_frame.layout.addWidget(self.control_frame)
        self.lower_frame.layout.addWidget(self.console_frame)
        self.lower_frame.layout.addStretch(1)
        self.lower_frame.layout.addWidget(self.status_frame)

        self.lower_frame.layout.setContentsMargins(0,0,0,0)
        self.lower_frame.setLayout(self.lower_frame.layout)


        self.frame = QWidget()
        self.frame.layout = QVBoxLayout()
        
        self.frame.layout.addWidget(self.timer_frame)
        self.frame.layout.addWidget(self.grid, 100)
        self.frame.layout.addWidget(self.lower_frame)

        self.frame.layout.setContentsMargins(0,0,0,0)
        self.frame.setLayout(self.frame.layout)

        self.setCentralWidget(self.frame)



        self.status_updater = QTimer()
        self.status_updater.timeout.connect(self.update_status)
        self.status_updater.start(100)

    def update_status(self):
        if self.grid.front_cam.connected:
            self.status.front_cam_status.set_connected()
        else:
            self.status.front_cam_status.set_disconnected()

        if self.grid.down_cam.connected:
            self.status.down_cam_status.set_connected()
        else:
            self.status.down_cam_status.set_disconnected()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_C:
            timestamp = datetime.now().strftime(f'%d-%m-%y_%H:%M:%S.%f')[:-4]
            os.mkdir(f'captures/{timestamp}')

            try:
                filename = f'captures/{timestamp}/front_camera.png'
                cv2.imwrite(filename, self.grid.front_cam.thread.image)


                # logging.info(f'Captured: captures/{timestamp}.png')
            except cv2.error:
                # logging.error('Camera has not yet loaded, please wait')
                pass

            try:
                filename = f'captures/{timestamp}/down_camera.png'
                cv2.imwrite(filename, self.grid.down_cam.thread.image)


                # logging.info(f'Captured: captures/{timestamp}.png')
            except cv2.error:
                # logging.error('Camera has not yet loaded, please wait')
                pass

            print(os.listdir(f'captures/{timestamp}'))
            


if __name__ == '__main__':
    with open('settings.yml', 'r') as f:
        settings = yaml.safe_load(f)

    app = QApplication([])
    app.setStyle('Fusion')

    window = CrimsonUI(int(settings['camera-ports']['front']), int(settings['camera-ports']['down']))
    window.show()

    sys.exit(app.exec())

