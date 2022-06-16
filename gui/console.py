from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPlainTextEdit, QDialog, QLineEdit, QLabel
from PyQt5.QtCore import Qt

import os
import shutil

import logging

from datetime import datetime

class ConsoleModule(QWidget):
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

        self.logs = Logs()
        self.command_line = CommandLine()


        self.layout = QVBoxLayout()

        self.layout.addWidget(self.logs, 100)
        self.layout.addWidget(self.command_line)

        self.layout.setContentsMargins(0,0,0,0)

        self.setLayout(self.layout)

class LoggerBox(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.logger = QPlainTextEdit()
        self.logger.setReadOnly(True)

    
    def emit(self, record):
        self.msg = self.format(record)
        self.logger.appendPlainText(self.msg)


class Logs(QDialog, QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QPlainTextEdit {
                font: 12px;
                color: white
            }

            QScrollBar:handle {
                background: rgb(35, 35, 35);
                border-radius: 5px
            }

            QScrollBar:up-arrow, QScrollBar:down-arrow {
                height: 0px;
                width: 0px;
                background: rgb(26, 26, 26)
            }
        """)

        self.logger = LoggerBox(self)
        self.logger.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S'))

        logging.getLogger().addHandler(self.logger)
        logging.getLogger().setLevel(logging.DEBUG)
        

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logger.logger)

        self.setLayout(self.layout)

    def reject(self):
        pass


class CommandLine(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background: rgb(35, 35, 35);
                padding: 5px;

                border-top-left-radius: 10px;
                border-top-right-radius: 10px;

                color: rgb(200, 200, 200)
            }
        """)

        self.key_logging = False

        self.setPlaceholderText('"help" for commands')
        self.setAttribute(Qt.WA_MacShowFocusRect, False) # Mac only
        self.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)

        self.returnPressed.connect(self.command_event)

    def command_event(self):
        self.clearFocus()

        split_text = self.text().split(' ')

        self.clear()

        if split_text[0] == 'help':
            logging.info("""

            Commands:
            "help" - shows this menu
            "return (++)" - returns text to logs
            "exit" - stops the program

            "list" - list all folders in
            the captures directory
            "empty" - permanently empties
            the captures directory
            "key" - toggles key logging

            Key:
            '()' = required
            '[]' = optional
            '+' = any value
            '++' = one or more values
            """)

        elif split_text[0] == 'return':
            if not len(split_text) > 1:
                logging.error('Please provide additional argument(s)')
            else:
                logging.info(' '.join(split_text[1:]))


        elif split_text[0] == 'exit':
            print('\033[93m\033[1mSuccessfully stopped Crimson UI\033[0m')

            exit()

        elif split_text[0] == 'list':
            captures_dir = sorted([f for f in os.listdir('captures/')])

            

            if captures_dir:
                stringed_captures = "\n".join(captures_dir)
                logging.info(f'captures/\n{stringed_captures}')
            else:
                logging.info('The captures directory is empty!')

        elif split_text[0] == 'empty':
            shutil.rmtree('captures')
            os.mkdir('captures')

            logging.info('Successfully emptied the captures directory')

        elif split_text[0] == 'key':
            if self.key_logging:
                self.key_logging = False
            else:
                self.key_logging = True
            
            logging.info(f'Key logging: {self.key_logging}')
        
        else:
            logging.error(f'Command "{split_text[0]}" does not exist')