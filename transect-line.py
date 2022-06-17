import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import thrusters

hsv = None
img = None
bounding_rect = None
empty = None
cam_dex = 0
baud_rate = 115200
thrust_manager = thrusters.ThrustManager()
error_queue = None
target_orientation = 0
current_orientation = None  #link controls orientation list here
# BECAUSE PARAMETERS ARE CRINGE

def detect_rope():
    global hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    mask_red = mask0+mask1
    hsv[np.where(mask_red==0)] = 0
    
def find_defect():
    global bounding_rect, empty
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        empty = True
        return (0, 0)
    
    cnt = contours[0]
    hull = cv2.convexHull(cnt, returnPoints = False)
    defects = cv2.convexityDefects(cnt, hull)
    
    if not defects:
        return (-1, -1)
    
    defect = defects[0, 0]
    bounding_rect = cv2.boundingRect(cnt)
    defect_pt = tuple(cnt[defect[2]][0])
    return defect_pt

def read_frame():
    global img, hsv
    vid = cv2.VideoCapture(cam_dex)
    _, img = vid.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
def turn(direction):
    left = False
    right = True
    
    if direction == left:
        #packet = 
    elif direction == right:
        #packet = 
        
    send_packet()
    time.sleep((len(packet)+2)/baud_rate)
    get_orientation_data()
    
    # Get angular acceleration data, then do 0.5at2 and figure out t
    
def adjust_orientation(orientation):
    orientation %= 360
    if (orientation < 0):
        orientation += 360
    return orientation

def get_error(current_orientation, target_orientation):
    error = adjust_orientation(target_orientation - current_orientation[0])
    if (error > 180):
        error = 180 - error
    return error

def run():
    finished = False
    thrust_manager.multiplier = 0.1
    thrust_manager.getTSpeeds((0, 1, 0), (0, 0, 0))    # Move forward

    while(not finished):
        read_frame()
        detect_rope()
        defect_pt = find_defect()
        
        if defect_pt == (0, 0):
            
            finished = True
        elif defect_pt != (-1, -1):
            x, y, w, h = bounding_rect
            thrust_manager.multiplier = 0.1 #stop moving forward
            thrust_manager.getTSpeeds((0, 0, 0), (0, 0, 0)) # Stop moving forward
            left = False
            right = True

            if ((defect_pt[0] - x) > (w / 2.0)):
                target_orientation = current_orientation[0] + 90 #turn left
                target_orientation = adjust_orientation(target_orientation)
                #START ERROR READING IN QUEUE, DON'T READ HERE PROBABLY
                error = adjust_orientation(target_orientation - current_orientation[0])
            else:
                turn(right);    #turn right

        