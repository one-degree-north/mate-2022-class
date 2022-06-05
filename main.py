from PyQt5.QtWidgets import QApplication

from gui.windows.front_camera import FrontCamera

import sys

# global timer, declare variable with snapshot of unix timestamp and display the difference
# ^ might not work for pause / will be very confusing

if __name__ == '__main__':
    app = QApplication([])

    window = FrontCamera()
    window.show()

    sys.exit(app.exec())