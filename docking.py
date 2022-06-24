import cv2
import numpy as np

class Docking:
    def __init__(self, img_path):
        self.img = cv2.imread(img_path)
        self.height, self.width, self.channels = self.img.shape
        self.centre = (int(width/2), int(height/2))
        
    def detect_diff(self):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        mask_red = mask0+mask1
        hsv[np.where(mask_red==0)] = 0
        
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 10, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        x, y, w, h = np.asarray(cv2.bounding_rectangle(max(contours, key = cv2.contourArea)))
        
        if abs(x + w/2 - self.centre[0]) > 0.1*self.width:
            # turn left/right for 0.05 seconds
            # move forward for 0.15 seconds
            
        if abs(y + h/2 - self.centre[1]) > 0.1*self.height:
            # up/down for 0.05 seconds
            # move forward for 0.15 secoinds
            
        if w >= self.width/2:
            return False
        
        return True
        
    def run(self):
        running = True
        while running:
            self.detect_diff()