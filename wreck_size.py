import cv2
import matplotlib.pyplot as plt
import numpy as np

class WreckSize:
    def __init__(self, path, gaussian_blur_filter = 5):
        self.img = cv2.imread(path)
        self.filter_size = gaussian_blur_filter
        self.lower_black = np.array([0, 0, 0])
        self.upper_black = np.array([350, 55, 100])
        
    def preprocess_image(self, img, filter_size):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_hsv = cv2.GaussianBlur(img_hsv, (filter_size, filter_size), 0)
        return img_hsv
    
    def save_fish_img(self, fish_rect, img_hsv):
        x, y, w, h = fish_rect
        img_rgb = cv2.cvtColor(img_hsv[y:y+h, x:x+w], cv2.COLOR_HSV2BGR)
        cv2.imwrite("Fish.png", img_rgb)
    
    def find_wreck(self, img_hsv):
        mask = cv2.inRange(img_hsv, self.lower_black, self.upper_black)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        wreck = max(contours, key = cv2.contourArea)
        rect = cv2.minAreaRect(wreck)
        return rect
    
    def find_length(self, rect):
        (x, y), (width, height), angle = rect
        ratio = max(width, height) / min(width, height)
        actual_width = 33.6
        return ratio * actual_width
    
    def run(self):
        self.frame_hsv = self.preprocess_image(self.img, self.filter_size)
        self.wreck = self.find_wreck(self.frame_hsv)
        return self.find_length(self.wreck)
