from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation

from gui.grid import CameraGrid
from gui.control import ControlBar
from gui.status import StatusBar
from gui.stopwatch import Stopwatch, StopwatchControlBar
from gui.capture import CaptureControlBar
from gui.console import ConsoleModule
from gui.info import ThrusterDisplayModule, AxisDisplayModule

from gui.automation_control import AutomationControlBar
from gui.preview import PreviewWidget

import sys
import os

import logging
import yaml
import cv2

class MainWindow(QMainWindow):
    def __init__(self, front_port, down_port):
        super().__init__()

        self.setWindowTitle('Crimson UI')

        self.setStyleSheet("""
            QMainWindow {
                background: rgb(21, 21, 21)
            }
        """)

        self.grid = CameraGrid(self, front_port, down_port)
        self.control = ControlBar(self)
        self.status = StatusBar()
        self.stopwatch = Stopwatch()
        self.stopwatch_control = StopwatchControlBar(self)
        self.capture_control = CaptureControlBar(self)

        self.console = ConsoleModule()
        self.console.hide()
        
        self.thruster_display = ThrusterDisplayModule()
        self.thruster_display.hide()

        self.axis_display = AxisDisplayModule()
        self.axis_display.hide()

        # self.stopwatch_status = QLabel('(T)')
        # self.stopwatch_status.setStyleSheet("""
        #     QLabel {
        #         margin-top: 10px;

        #         font: bold 10px;
        #         color: white
        #     }
        # """)

        # self.stopwatch_status.setAlignment(Qt.AlignRight)


        self.control_frame = QWidget()
        self.control_frame.layout = QVBoxLayout()
        
        self.control_frame.layout.addStretch(1)
        self.control_frame.layout.addWidget(self.control)

        self.control_frame.layout.setContentsMargins(0,0,0,0)
        self.control_frame.setLayout(self.control_frame.layout)


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


        self.stopwatch_frame = QWidget()
        self.stopwatch_frame.layout = QHBoxLayout()
        self.stopwatch_frame.layout.setSpacing(20)
        
        self.stopwatch_frame.layout.addWidget(self.stopwatch)
        self.stopwatch_frame.layout.addStretch(1)
        # self.stopwatch_frame.layout.addWidget(self.stopwatch_status)
        self.stopwatch_frame.layout.addWidget(self.capture_control)
        self.stopwatch_frame.layout.addWidget(self.stopwatch_control)

        self.stopwatch_frame.layout.setContentsMargins(0,0,0,0)
        self.stopwatch_frame.setLayout(self.stopwatch_frame.layout)


        self.lower_frame = QWidget()
        self.lower_frame.setFixedHeight(208)
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
        
        self.frame.layout.addWidget(self.stopwatch_frame)
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
        if self.console.command_line.key_logging and e.text().isprintable() and len(e.text()) == 1:
            logging.debug(f'{e.text()} ({ord(e.text())})')

class AutomationWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setWindowTitle('Crimson UI')

        self.setStyleSheet("""
            QWidget {
                background: rgb(21, 21, 21)
            }
        """)

        self.automation_control = AutomationControlBar()
        # self.preview_widget = PreviewWidget()

        self.automation_control_frame = QWidget()
        self.automation_control_frame.layout = QVBoxLayout()
        
        self.automation_control_frame.layout.addStretch(1)
        self.automation_control_frame.layout.addWidget(self.automation_control)

        self.automation_control_frame.layout.setContentsMargins(0,0,0,0)
        # self.automation_control_frame.setLayout(self.automation_control_frame.layout)

        # self.preview_frame = QWidget()
        # self.preview_frame.layout = QVBoxLayout()
        
        # self.preview_frame.layout.addWidget(self.preview_widget)

        self.setLayout(self.automation_control_frame.layout)



if __name__ == '__main__':
    with open('settings.yml', 'r') as f:
        settings = yaml.safe_load(f)


    app = QApplication([])
    app.setStyle('Fusion')

    main = MainWindow(int(settings['camera-ports']['front']), int(settings['camera-ports']['down']))
    main.show()

    # automation = AutomationWindow()
    # automation.show()

    try:
        os.mkdir('captures')
        logging.warning('No captures directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    logging.info('Successfully loaded Crimson UI')

    sys.exit(app.exec())

