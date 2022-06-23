import cv2
import matplotlib.pyplot as plt
import numpy as np
import time

class TransectLine:
    def __init__(self, cam_dex, delay): # Delay in seconds
        self.vid = cv2.VideoCapture(cam_dex)
        self.delay = delay
        
    def detect_rope(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        mask_red = mask0+mask1
        hsv[np.where(mask_red==0)] = 0

        return rope_hsv

    def find_defect(self, rope_hsv):
        rgb = cv2.cvtColor(rope_hsv, cv2.COLOR_HSV2RGB)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return (0, 0)

        cnt = max(contours, key = cv2.contourArea)
        hull = cv2.convexHull(cnt, returnPoints = False)
        defects = cv2.convexityDefects(cnt, hull)

        if not defects:
            return (-1, -1)

        defect = defects[0, 0]
        defect_pt = tuple(cnt[defect[2]][0])
        return defect_pt

    def turn(self, direction):
        left, right = False, True

        if direction == left:
            # Turn left 
        elif direction == right:
            # Turn right

    def move_forward(self, move: bool):
        # Kevin: finish this part

    def wait_for_turns(self, delay):
        defect_pt = (-1, -1)

        while defect_pt is (-1, -1):
            _, frame_hsv = self.vid.read()
            rope_hsv = self.detect_rope(frame_hsv[0 : round(frame_hsv.shape[0]/2]))
            defect_pt = self.find_defect(rope_hsv)
            time.sleep(delay)

        move_forward(False)

    def run(self):
        left, right = False, True
        self.move_forward(True)
        self.wait_for_turns(self.delay)
        self.turn(right)
        self.move_forward(True)
        self.wait_for_turns(self.delay)
        self.turn(right)
        self.move_forward(True)
        self.wait_for_turns(self.delay)
        self.turn(left)
        self.move_forward(True)
        self.wait_for_turns(self.delay)
        self.turn(left)
        self.move_forward(True)
        self.wait_for_turns(self.delay)
