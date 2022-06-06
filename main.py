from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from gui.windows.home import MainWindow

import sys
# from time import sleep

# global timer, declare variable with snapshot of unix timestamp and display the difference
# ^ might not work for pause / will be very confusing
# use qtimer

# class LoadingWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setFixedSize(300,200)

#         self.setStyleSheet("""
#             QMainWindow {

#             }
#         """)

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    # loading = LoadingWindow()
    # loading.show()

    # sleep(10)
    # loading.hide()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())