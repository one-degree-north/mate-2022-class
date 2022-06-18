from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from unify import Unifiy

import sys
import os

import queue
import logging
import yaml

from threading import Thread

def unify_listener():
    while True:
        if q_out.qsize() != 0:
            output = q_out.get()
            main.update_thruster_values(output[0])
            main.update_axis_values(output[1])

if __name__ == '__main__':
    with open('settings.yml', 'r') as f:
        settings = yaml.safe_load(f)
    
    q = queue.Queue()
    q_out = queue.Queue()

    app = QApplication([])
    app.setStyle('Fusion')

    main = MainWindow(int(settings['camera-ports']['front']), int(settings['camera-ports']['down']))#, q_out)
    main.show()

    unify_listener_thread = Thread(target=unify_listener, daemon=True)
    unify_listener_thread.start()

    unifiy = Unifiy(q, q_out, 10)
    unifiy.initiateWrangling()

    try:
        os.mkdir('captures')
        logging.warning('No captures directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    logging.info('Successfully loaded Crimson UI')

    sys.exit(app.exec())

