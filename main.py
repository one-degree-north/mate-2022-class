from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from unify import Unify

import sys
import os

import queue
import logging
import yaml

from threading import Thread
from time import sleep

def unify_listener():
    while True:
        if guiQueue.qsize() != 0:
            output = guiQueue.get()
            main.update_thruster_values(output[0])
            main.update_axis_values(output[1])

            sleep(0.01)

if __name__ == '__main__':
    from controls import Controls
    controls = None  
    controls = Controls()
    controls.comms.startThread()


    with open('settings.yml', 'r') as f:
        settings = yaml.safe_load(f)
    
    requestQueue = queue.Queue()
    guiQueue = queue.Queue()

    app = QApplication([])
    app.setStyle('Fusion')

    main = MainWindow(int(settings['camera-ports']['front']), int(settings['camera-ports']['down']))
    main.show()

    unify_listener_thread = Thread(target=unify_listener, daemon=True)
    unify_listener_thread.start()

    unify = Unify(requestQueue=requestQueue, guiQueue=guiQueue, interval=10, controls=controls)
    unify.start()

    try:
        os.mkdir('captures')
        logging.warning('No captures directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    print('\033[92m\033[1mSuccessfully loaded Crimson UI\033[0m')
    logging.info('Successfully loaded Crimson UI')

    sys.exit(app.exec())

