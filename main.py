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
from controls import Controls

# def unify_listener():
#     while True:
#         if guiQueue.qsize() != 0:
#             output = guiQueue.get()
#             window.update_thruster_values(output[0])
#             window.update_axis_values(output[1])

#             sleep(0.01)

if __name__ == '__main__':
    controls = None  
    # controls = Controls()
    # controls.comms.startThread()

    with open('settings.yml', 'r') as f:
        settings = yaml.safe_load(f)


    app = QApplication([])
    app.setStyle('Fusion')

    requestQueue = queue.Queue()
    guiQueue = queue.Queue()

    window = MainWindow(int(settings['camera-ports']['front']), int(settings['camera-ports']['down']))
    u = Unify(requestQueue=requestQueue, guiQueue=guiQueue, interval=10, controls=controls)

    try:
        os.mkdir('captures')
        logging.warning('No captures directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    try:
        os.mkdir('captures/IMAGES')
        logging.warning('No images directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    try:
        os.mkdir('captures/VIDEOS')
        logging.warning('No videos directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    # unify_listener_thread = Thread(target=unify_listener, daemon=True)
    # unify_listener_thread.start()

    print('\033[92m\033[1mSuccessfully loaded Crimson UI\033[0m')
    logging.info('Successfully loaded Crimson UI')

    window.show()
    u.start()

    sys.exit(app.exec())

