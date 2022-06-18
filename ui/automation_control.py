from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from .button import Button

class AutomationControlBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-right-radius: 10px
            }
        """)

        self.docking_button = Button('ui/icons/docking_icon.png', 'Autonomous docking')
        self.docking_button.clicked.connect(self.docking)

        self.transect_button = Button('ui/icons/transect_icon.png', 'Transect line')
        self.transect_button.clicked.connect(self.transect)

        self.morts_button = Button('ui/icons/morts_icon.png', 'Differentiate morts')
        self.morts_button.clicked.connect(self.morts)

        self.measure_button = Button('ui/icons/measure_icon.png', 'Measure fish size')
        self.measure_button.clicked.connect(self.measure)

        self.endurance_button = Button('ui/icons/Endurance_icon.png', 'Transect over Endurance area')
        self.endurance_button.clicked.connect(self.endurance)

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
        print('transect')
        pass

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
        print('not ok')
        pass

    def photomosaic(self):
        print('photomosaic')
        pass
