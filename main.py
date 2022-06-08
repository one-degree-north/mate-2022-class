from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget


from gui.grid import Grid
from gui.control import ControlBar
from gui.status import StatusBar
from gui.timer import TimerBar

import sys
import yaml

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


        # Control frame
        self.control_frame = QWidget()

        self.control_frame.layout = QVBoxLayout()
        
        self.control_frame.layout.addStretch(1)
        self.control_frame.layout.addWidget(self.control)

        self.control_frame.layout.setContentsMargins(0,0,0,0)
        self.control_frame.setLayout(self.control_frame.layout)


        # Status frame
        self.status_frame = QWidget()

        self.status_frame.layout = QVBoxLayout()
        
        self.status_frame.layout.addStretch(1)
        self.status_frame.layout.addWidget(self.status)

        self.status_frame.layout.setContentsMargins(0,0,0,0)
        self.status_frame.setLayout(self.status_frame.layout)


        # Timer frame
        self.timer_frame = QWidget()

        self.timer_frame.layout = QHBoxLayout()
        
        self.timer_frame.layout.addWidget(self.timer)
        self.timer_frame.layout.addStretch(1)

        self.timer_frame.layout.setContentsMargins(0,0,0,0)
        self.timer_frame.setLayout(self.timer_frame.layout)


        # Lower frame
        self.lower = QWidget()

        self.lower.layout = QHBoxLayout()

        self.lower.layout.addWidget(self.control_frame)
        self.lower.layout.addWidget(self.grid, 100)
        self.lower.layout.addWidget(self.status_frame)

        self.lower.layout.setContentsMargins(0,0,0,0)
        self.lower.setLayout(self.lower.layout)


        # Parent frame
        self.frame = QWidget()

        self.frame.layout = QVBoxLayout()
        
        self.frame.layout.addWidget(self.timer_frame)
        self.frame.layout.addWidget(self.lower, 100)

        self.frame.layout.setContentsMargins(0,0,0,0)
        self.frame.setLayout(self.frame.layout)

        self.setCentralWidget(self.frame)

if __name__ == '__main__':
    with open('settings.yml', 'r') as f:
        settings = yaml.safe_load(f)

    app = QApplication([])
    app.setStyle('Fusion')

    window = CrimsonUI(int(settings['camera-ports']['front']), int(settings['camera-ports']['down']))
    window.show()

    sys.exit(app.exec())