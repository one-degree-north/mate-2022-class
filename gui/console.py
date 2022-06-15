from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPlainTextEdit, QDialog, QLineEdit, QLabel
from PyQt5.QtCore import Qt

import os
from datetime import datetime

import logging

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

        for _ in range(50):
            logging.debug('ok')

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
        self.split_text = self.text().split(' ')

        self.clear()

        if self.split_text[0] == 'help':
            # logging.info(f"""
            #     Hotkeys:
            #     ` - shows/hides the tab bar (if styled)
            #     t - toggles between styled tabs and regular tabs (styled by default)
            #     l - shows mini-logs in tab bar (styled menu only)
            #     1 through 3 - switches active tab
                # c - capture a screenshot

            logging.info("""

            Commands:
            help - shows this menu
            return (++) - returns text to logs
            exit - stops the program
            key - toggles key logging


            Key:
            "()" = required
            "[]" = optional
            "+" = any value
            "++" = one or more values
            """)

        elif self.split_text[0] == 'return':
            if not len(self.split_text) > 1:
                logging.error('Please provide additional argument(s)')
            else:
                logging.info(' '.join(self.split_text[1:]))


        elif self.split_text[0] == 'exit':
            print('\033[93m\033[1mSuccessfully stopped Crimson UI\033[0m')

            exit()

        elif self.split_text[0] == 'key':
            logging.info('keylogging')



        # elif self.split_text[0] == 'ping':
        #     pass
        
        # elif self.split_text[0] == 'clear':
        #     pass
        
        else:
            logging.error(f'Command "{self.split_text[0]}" does not exist')