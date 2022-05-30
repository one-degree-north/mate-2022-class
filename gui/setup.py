from PyQt5.QtWidgets import QApplication

import sys

from windows.front_cam import FrontCamera





# class ClawCamera(Camera(1)):
#     def __init__(self):
#         super().__init__()
        
#         self.layout = QHBoxLayout()
#         self.layout.addWidget(QLabel('ok'))

#         self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication([])

    window = FrontCamera()
    window.show()

    sys.exit(app.exec())