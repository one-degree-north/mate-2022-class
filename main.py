from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from unify import Unifiy

import sys
import os

import queue
import logging
import yaml
import cv2

from threading import Thread

# def update_status(self):
#     if self.grid.front_cam.connected:
#         self.status.front_cam_status.set_connected()
#     else:
#         self.status.front_cam_status.set_disconnected()

#     if self.grid.down_cam.connected:
#         self.status.down_cam_status.set_connected()
#     else:
#         self.status.down_cam_status.set_disconnected()

#     def update_thruster_values(self, values_dict):
#         self.thruster_display.front_left_thruster_label.update_value(round(values_dict[0]*100, 1))
#         self.thruster_display.front_right_thruster_label.update_value(round(values_dict[1]*100, 1))
#         self.thruster_display.back_left_thruster_label.update_value(round(values_dict[2]*100, 1))
#         self.thruster_display.back_right_thruster_label.update_value(round(values_dict[3]*100, 1))
#         self.thruster_display.left_thruster_label.update_value(round(values_dict[4]*100, 1))
#         self.thruster_display.right_thruster_label.update_value(round(values_dict[5]*100, 1))

#     def update_axis_values(self, values_dict):
#         self.axis_display.roll_label.update_value(round(values_dict[0]*100, 1))
#         self.axis_display.pitch_label.update_value(round(values_dict[1]*100, 1))
#         self.axis_display.yaw_label.update_value(round(values_dict[2]*100, 1))

    # def listenForThrusterSpeeds(self):
    #     while True:
    #         # print(self.KrishnaQ.qsize())
    #         if self.KrishnaQ.qsize() != 0:
    #             # print("getting")
    #             KQoutput = self.KrishnaQ.get()
    #             # print(KQoutput)
    #             # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #             self.update_thruster_values(KQoutput[0])
    #             self.update_axis_values(KQoutput[1])

            
    # def startKrishnaQListener(self):
    #     l = threading.Thread(target=self.listenForThrusterSpeeds)
    #     l.start()

    # def keyPressEvent(self, event):

    #     if self.console.command_line.key_press_logging and event.text().isprintable() and len(event.text()) == 1:
    #         logging.debug(f'Press: {event.text()} ({ord(event.text())})')

    # def keyReleaseEvent(self, event):

    #     if self.console.command_line.key_release_logging and event.text().isprintable() and len(event.text()) == 1:
    #         logging.debug(f'Release: {event.text()} ({ord(event.text())})')

# def update_thruster_values(values_dict):
#     main.thruster_display.front_left_thruster_label.update_value(round(values_dict[0]*100, 1))
#     main.thruster_display.front_right_thruster_label.update_value(round(values_dict[1]*100, 1))
#     main.thruster_display.back_left_thruster_label.update_value(round(values_dict[2]*100, 1))
#     main.thruster_display.back_right_thruster_label.update_value(round(values_dict[3]*100, 1))
#     main.thruster_display.left_thruster_label.update_value(round(values_dict[4]*100, 1))
#     main.thruster_display.right_thruster_label.update_value(round(values_dict[5]*100, 1))

# def update_axis_values(values_dict):
#     main.axis_display.roll_label.update_value(round(values_dict[0]*100, 1))
#     main.axis_display.pitch_label.update_value(round(values_dict[1]*100, 1))
#     main.axis_display.yaw_label.update_value(round(values_dict[2]*100, 1))

def unify_listener():
    while True:
        if q_out.qsize() != 0:
            output = q_out.get()
            main.update_thruster_values(output[0])
            main.update_axis_values(output[1])

# def qt_listener():
#     while True:
#         if main.grid.front_cam.connected:
#             main.status.front_cam_status.set_connected()
#         else:
#             main.status.front_cam_status.set_disconnected()

#         if main.grid.down_cam.connected:
#             main.status.down_cam_status.set_connected()
#         else:
#             main.status.front_cam_status.set_disconnected()
        
#         sleep(0.01) ##
        
# class Listener(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#         self.daemon = True
#         self.start()

#     def run(self):
#         while True:
#             if q_out.qsize() != 0:
#                 output = q_out.get()
#                 update_thruster_values(output[0])
#                 update_axis_values(output[1])
            
#             if main.grid.front_cam.connected:
#                 main.status.front_cam_status.set_connected()
#             else:
#                 main.status.front_cam_status.set_disconnected()

#             if main.grid.down_cam.connected:
#                 main.status.down_cam_status.set_connected()
#             else:
#                 main.status.front_cam_status.set_disconnected()
            
#             sleep(0.01)
        

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

    # qt_listener_thread = Thread(target=qt_listener, daemon=True)
    # qt_listener_thread.start()

    unifiy = Unifiy(q, q_out, 10)
    unifiy.initiateWrangling()

    try:
        os.mkdir('captures')
        logging.warning('No captures directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    logging.info('Successfully loaded Crimson UI')

    sys.exit(app.exec())

