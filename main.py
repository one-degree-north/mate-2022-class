from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation

from gui.grid import Grid
from gui.control import ControlBar
from gui.status import StatusBar
from gui.timer import TimerBar, TimerControlBar
from gui.console import ConsoleModule
from gui.info import ThrusterDisplayModule, AxisDisplayModule

import sys
import os

import yaml
import cv2

from datetime import datetime

# class Title(QLabel):
#     def __init__(self):
#         super().__init__('Octopus Prime')

#         self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

#         self.setStyleSheet("""
#             QWidget {
#                 background: rgb(26, 26, 26);
#                 border-bottom-left-radius: 10px;
#                 border-bottom-right-radius: 10px;

#                 font: bold 30px;
#                 color: white
#             }
#         """)

# self.animation = QPropertyAnimation(self.menu, b'pos')
# self.animation.setStartValue(QPoint(-260,self.pos))
# self.animation.setEndValue(QPoint(0,0))
# self.animation.setDuration(200)
# self.animation.start()

# else:
# self.animation = QPropertyAnimation(self.menu, b'pos')
# self.animation.setStartValue(QPoint(0,0))
# self.animation.setEndValue(QPoint(-260,0))
# self.animation.setDuration(200)
# self.animation.start()

# self.animation.finished.connect(lambda: self.menu.hide())

class CrimsonUI(QMainWindow):
    def __init__(self, front_port, down_port):
        super().__init__()

        self.setWindowTitle('Crimson UI')

        self.setStyleSheet("""
            QMainWindow {
                background: rgb(21, 21, 21)
            }
        """)

        self.grid = Grid(front_port, down_port)
        self.control = ControlBar(self)
        self.status = StatusBar()
        self.timer = TimerBar()
        self.timer_control = TimerControlBar(self)

        self.console = ConsoleModule()
        self.console.hide()
        
        self.thruster_display = ThrusterDisplayModule()
        self.thruster_display.hide()

        self.axis_display = AxisDisplayModule()
        self.axis_display.hide()


        self.control_frame = QWidget()
        self.control_frame.layout = QVBoxLayout()
        
        self.control_frame.layout.addStretch(1)
        self.control_frame.layout.addWidget(self.control)

        self.control_frame.layout.setContentsMargins(0,0,0,0)
        self.control_frame.setLayout(self.control_frame.layout)


        # self.console_frame = QWidget()
        # self.console_frame.layout = QVBoxLayout()
        
        # self.console_frame.layout.addStretch(1)
        # self.console_frame.layout.addWidget(self.console)

        # self.console_frame.layout.setContentsMargins(0,0,0,0)
        # self.console_frame.setLayout(self.console_frame.layout)

        self.thruster_display_frame = QWidget()
        self.thruster_display_frame.layout = QVBoxLayout()
        
        self.thruster_display_frame.layout.addStretch(1)
        self.thruster_display_frame.layout.addWidget(self.thruster_display)

        self.thruster_display_frame.layout.setContentsMargins(0,0,0,0)
        self.thruster_display_frame.setLayout(self.thruster_display_frame.layout)


        self.axis_display_frame = QWidget()
        self.axis_display_frame.layout = QVBoxLayout()
        
        self.axis_display_frame.layout.addStretch(1)
        self.axis_display_frame.layout.addWidget(self.axis_display)

        self.axis_display_frame.layout.setContentsMargins(0,0,0,0)
        self.axis_display_frame.setLayout(self.axis_display_frame.layout)


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
        # self.timer_frame.layout.addWidget(self.title)
        # self.timer_frame.layout.addStretch(1)

        self.timer_frame.layout.addWidget(self.timer_control)

        self.timer_frame.layout.setContentsMargins(0,0,0,0)
        self.timer_frame.setLayout(self.timer_frame.layout)


        self.lower_frame = QWidget()

        self.lower_frame.setFixedHeight(250)

        self.lower_frame.layout = QHBoxLayout()
        self.lower_frame.layout.setSpacing(20)

        self.lower_frame.layout.addWidget(self.control_frame)
        self.lower_frame.layout.addWidget(self.console)
        self.lower_frame.layout.addWidget(self.thruster_display_frame)
        self.lower_frame.layout.addStretch(1)
        self.lower_frame.layout.addWidget(self.axis_display_frame)
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

        else:
            pass
            


if __name__ == '__main__':
    with open('settings.yml', 'r') as f:
        settings = yaml.safe_load(f)

    app = QApplication([])
    app.setStyle('Fusion')

    window = CrimsonUI(int(settings['camera-ports']['front']), int(settings['camera-ports']['down']))
    window.show()

    sys.exit(app.exec())

