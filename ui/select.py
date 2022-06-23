from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QLabel, QScrollArea
from PyQt5.QtCore import Qt

from .button import Button

class SelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            background: rgb(26, 26, 26);
            border-radius: 10px;
            margin: 10px;

            color: white
        """)

        self.scrolling_label = ScrollingLabel()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scrolling_label)

        self.setLayout(self.layout)

class ScrollingLabel(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        self.content = QWidget()
        self.setWidget(self.content)

        self.label = QLabel(self.content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.label.setWordWrap(True)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def setText(self, text):
        self.label.setText(text)