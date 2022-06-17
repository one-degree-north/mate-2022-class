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

        self.docking_button = Button('gui/icons/docking_icon.png', 'Autonomous docking')
        # self.help_button.clicked.connect(self.help)

        self.transect_button = Button('gui/icons/transect_icon.png', 'Transect line')
        # self.info_button.clicked.connect(self.info)

        self.morts_button = Button('gui/icons/morts_icon.png', 'Differentiate morts')
        # self.console_button.clicked.connect(self.console)

        self.measure_button = Button('gui/icons/measure_icon.png', 'Measure fish size')
        # self.quit_button.clicked.connect(self.quit)

        self.endurance_button = Button('gui/icons/Endurance_icon.png', 'Transect over endurance area')
        # self.quit_button.clicked.connect(self.quit)

        self.measure_endurance_button = Button('gui/icons/measure_Endurance_icon.png', 'Measure endurance area')
        # self.quit_button.clicked.connect(self.quit)

        self.photomosaic_button = Button('gui/icons/photomosaic_icon.png', 'Photomosaic')
        # self.quit_button.clicked.connect(self.quit)



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
