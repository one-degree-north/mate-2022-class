# percentage of total movement, axis, rotation

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class ThrusterDisplayModule(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-left-radius: 10px;
                border-top-right-radius: 10px
            }
        """)

        self.left_thruster_label = StyledLabel('Left thruster', '%')
        self.right_thruster_label = StyledLabel('Right thruster', '%')

        self.front_left_thruster_label = StyledLabel('Front left thruster', '%')
        self.front_right_thruster_label = StyledLabel('Front right thruster', '%')
        self.back_left_thruster_label = StyledLabel('Back left thruster', ' %')
        self.back_right_thruster_label = StyledLabel('Back right thruster', '%')

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.left_thruster_label)
        self.layout.addWidget(self.right_thruster_label)

        self.layout.addWidget(self.front_left_thruster_label)
        self.layout.addWidget(self.front_right_thruster_label)
        self.layout.addWidget(self.back_left_thruster_label)
        self.layout.addWidget(self.back_right_thruster_label)

        self.setLayout(self.layout)


class AxisDisplayModule(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-left-radius: 10px;
                border-top-right-radius: 10px
            }
        """)

        self.roll_label = StyledLabel('Roll',  '°')
        self.pitch_label = StyledLabel('Pitch', '°')
        self.yaw_label = StyledLabel('Yaw', '°')

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.roll_label)
        self.layout.addWidget(self.pitch_label)
        self.layout.addWidget(self.yaw_label)

        self.setLayout(self.layout)

        
class StyledLabel(QLabel):
    def __init__(self, name, units):
        super().__init__(f'<b>{name}:</b> undef')

        self.name = name
        self.units = units

        self.setStyleSheet("""
            QLabel {
                font: 12px;
                color: white
            }
        """)

    def update_value(self, value):
        self.setText(f'<b>{self.name}:</b> {value}{self.units}')