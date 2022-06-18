from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

from ui.grid import CameraGrid
from ui.control import ControlBar
from ui.status import StatusBar
from ui.stopwatch import Stopwatch, StopwatchControlBar
from ui.capture import CaptureControlBar
from ui.console import ConsoleModule
from ui.info import ThrusterDisplayModule, AxisDisplayModule

from ui.automation_control import AutomationControlBar
from ui.preview import PreviewWidget

import logging

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

        self.automation_window = AutomationWindow(self)


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


        self.status_thread = QTimer()
        self.status_thread.timeout.connect(self.status_listener)
        self.status_thread.start(10)


    def status_listener(self):
        if self.grid.front_cam.connected:
            self.status.front_cam_status.set_connected()
        else:
            self.status.front_cam_status.set_disconnected()

        if self.grid.down_cam.connected:
            self.status.down_cam_status.set_connected()
        else:
            self.status.down_cam_status.set_disconnected()

    def update_thruster_values(self, values_dict):
        self.thruster_display.front_left_thruster_label.update_value(round(values_dict[0]*100, 1))
        self.thruster_display.front_right_thruster_label.update_value(round(values_dict[1]*100, 1))
        self.thruster_display.back_left_thruster_label.update_value(round(values_dict[2]*100, 1))
        self.thruster_display.back_right_thruster_label.update_value(round(values_dict[3]*100, 1))
        self.thruster_display.left_thruster_label.update_value(round(values_dict[4]*100, 1))
        self.thruster_display.right_thruster_label.update_value(round(values_dict[5]*100, 1))

    def update_axis_values(self, values_dict):
        self.axis_display.roll_label.update_value(round(values_dict[0]*100, 1))
        self.axis_display.pitch_label.update_value(round(values_dict[1]*100, 1))
        self.axis_display.yaw_label.update_value(round(values_dict[2]*100, 1))

    def keyPressEvent(self, event):
        if self.console.command_line.key_press_logging and event.text().isprintable() and len(event.text()) == 1:
            logging.debug(f'Press: {event.text()} ({ord(event.text())})')

    def keyReleaseEvent(self, event):
        if self.console.command_line.key_release_logging and event.text().isprintable() and len(event.text()) == 1:
            logging.debug(f'Release: {event.text()} ({ord(event.text())})')

class AutomationWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.setWindowTitle('Crimson UI (Automation)')

        self.setStyleSheet("""
            QWidget {
                background: rgb(21, 21, 21)
            }
        """)

        self.parent = parent

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
        # self.setCentralWidget(self.automation_control_frame)

    def closeEvent(self, event):
        self.parent.control.automation_button.setDisabled(False)
        event.accept()


