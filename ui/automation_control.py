from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt

from .button import Button

import sys
sys.path.append('..')

from wreck_size import WreckSize
from transect_line import TransectLine
from photomosaic import Photomosaic

class AutomationControlBar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-right-radius: 10px
            }
        """)

        self.parent = parent

        self.docking_button = Button('ui/icons/docking_icon.png', 'Autonomous docking')
        self.docking_button.clicked.connect(self.docking)
        self.docking_button.setDisabled(True)

        self.transect_button = Button('ui/icons/transect_icon.png', 'Transect line')
        self.transect_button.clicked.connect(self.transect)

        self.morts_button = Button('ui/icons/morts_icon.png', 'Differentiate morts')
        self.morts_button.clicked.connect(self.morts)
        self.morts_button.setDisabled(True)

        self.measure_button = Button('ui/icons/measure_icon.png', 'Measure fish size')
        self.measure_button.clicked.connect(self.measure)

        self.endurance_button = Button('ui/icons/Endurance_icon.png', 'Transect over Endurance area')
        self.endurance_button.clicked.connect(self.endurance)
        self.endurance_button.setDisabled(True)

        self.measure_endurance_button = Button('ui/icons/measure_Endurance_icon.png', 'Measure Endurance area')
        self.measure_endurance_button.clicked.connect(self.measure_endurance)

        self.photomosaic_button = Button('ui/icons/photomosaic_icon.png', 'Photomosaic')
        self.photomosaic_button.clicked.connect(self.photomosaic)



        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.docking_button)
        self.layout.addWidget(self.transect_button)
        self.layout.addWidget(self.morts_button)
        self.layout.addWidget(self.measure_button)
        self.layout.addWidget(self.endurance_button)
        self.layout.addWidget(self.measure_endurance_button)
        self.layout.addWidget(self.photomosaic_button)

        self.setLayout(self.layout)

        self.setFixedWidth(60)


    def docking(self):
        print('dock')
        pass

    def transect(self):
        TransectLine(self.parent.parent.grid.down_cam.thread.cap, 0.1)
        self.parent.selection.scrolling_label.setText('TRANSECT LINE')

    def morts(self):
        print('dead fish')
        pass

    def measure(self):
        print('measure')
        pass

    def endurance(self):
        print('ok')
        pass

    def measure_endurance(self):
        selection, _ = QFileDialog.getOpenFileName(self, 'Select image', 'captures/IMAGES', 'Images (*.png *.jpg)')

        if selection:
            self.parent.selection.scrolling_label.setText(f'MEASURE ENDURANCE\n{selection}')

            WreckSize(selection)

        # print(selection)

    def photomosaic(self):
        # print('photomosaic')
        # pass
        selections = []
        while len(selections) != 8:
            selection, _ = QFileDialog.getOpenFileName(self, f'Select image ({len(selections)}/8)', 'captures/IMAGES', 'Images (*.png *.jpg)')
            
            if selection:
                selections.append(selection)
                self.parent.selection.scrolling_label.setText(f'PHOTOMOSAIC\nAppended ({len(selections)}): {selection}')
            else:
                self.parent.selection.scrolling_label.setText(f'PHOTOMOSAIC\nexit')
                return
            
        self.parent.selection.scrolling_label.setText(f'PHOTOMOSAIC\n{selections}')
        Photomosaic(selections)

