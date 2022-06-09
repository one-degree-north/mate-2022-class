from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPlainTextEdit, QDialog, QLineEdit, QLabel
from PyQt5.QtCore import Qt

from .button import Button

import os
from datetime import datetime

import logging

class ControlBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-right-radius: 10px
            }
        """)

        self.help_button = Button('gui/icons/help_icon.png', 'Help')
        self.help_button.clicked.connect(self.help)

        self.console_button = Button('gui/icons/console_icon.png', 'Console')
        self.console_button.clicked.connect(self.console)

        self.console_window = ConsoleWindow()

        self.reconnect_button = Button('gui/icons/reload_icon.png', 'Reconnect')
        self.reconnect_button.clicked.connect(self.reconnect)

        self.quit_button = Button('gui/icons/quit_icon.png', 'Quit')
        self.quit_button.clicked.connect(self.quit)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.help_button)
        self.layout.addWidget(self.console_button)
        self.layout.addWidget(self.reconnect_button)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

        self.setFixedWidth(60)

    def help(self):
        pass

    def console(self):
        self.console_window.show()

    def reconnect(self):
        pass

    def quit(self):
        # access camera from other windows and close
        print('\033[93m\033[1mSuccessfully stopped Crimson UI\033[0m') 

        exit()


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
                background: rgb(26, 26, 26);
                border-radius: 5px;
                padding: 10px;
                margin: 10px
            }
        """)

        self.controls_logging = False
        self.key_logging = False

        self.setPlaceholderText('"help" for commands')
        self.setAttribute(Qt.WA_MacShowFocusRect, False) # Mac only
        self.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)

        self.returnPressed.connect(self.command_event)

    def command_event(self):
        self.split_text = self.text().split(' ')

        self.clear()

        if self.split_text[0] == 'help':
            logging.info(f"""
                Hotkeys:
                ` - shows/hides the tab bar (if styled)
                t - toggles between styled tabs and regular tabs (styled by default)
                l - shows mini-logs in tab bar (styled menu only)
                1 through 3 - switches active tab
                c - capture a screenshot
                Commands:
                help - shows this menu
                return (++) - returns text to logs
                save - save a transcript of the logs
                exit - stops the program
                controls - toggles key logging for control keys (off by default)
                key - toggles key logging for keys that aren't controls (off by default)
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

        elif self.split_text[0] == 'save':
            timestamp = datetime.now().strftime(f'%d-%m-%y_%H:%M:%S.%f')[:-4]
            logging.FileHandler(f'{timestamp}/ok.txt')

        elif self.split_text[0] == 'exit':
            print('\033[93m\033[1mAzure UI has stopped sucessfully\033[0m')

            exit()


        elif self.split_text[0] == 'controls':
            if self.controls_logging:
                self.controls_logging = False
            else:
                self.controls_logging = True

            logging.info('Toggled key logging (controls)')

        elif self.split_text[0] == 'key':
            if self.key_logging:
                self.key_logging = False
            else:
                self.key_logging = True

            logging.info('Toggled key logging (excluding controls)')



        # elif self.split_text[0] == 'ping':
        #     pass
        
        # elif self.split_text[0] == 'clear':
        #     pass
        
        else:
            logging.error(f'Command "{self.split_text[0]}" does not exist')


class ConsoleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(21, 21, 21);
                border-radius: 10px;
                margin: 20px
            }
        """)

        self.logs = Logs()
        self.command_line = CommandLine()


        self.layout = QVBoxLayout()


        self.layout.addWidget(self.logs)
        self.layout.addWidget(self.command_line)

        self.layout.setSpacing(0)

        self.setLayout(self.layout)