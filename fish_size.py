import cv2
import matplotlib.pyplot as plt
import numpy as np

class FishSize:
    def __init__(self, read_path, write_path, gaussian_blur_filter):
        self.img = cv2.imread(path)
        self.write_path = write_path
        self.filter = gaussian_blur_filter
        self.lower_blue = np.array([45, 50, 50])
        self.upper_blue = np.array([125, 255, 255])
        
    def preprocess_image(self, img, filter_size = 5):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_hsv = cv2.GaussianBlur(img_hsv, (filter_size, filter_size), 0)
        return img_hsv
    
    def filter_out_water(self, img_hsv):
        mask = cv2.inRange(img_hsv, self.lower_blue, self.upper_blue)
        img_hsv[np.where(mask!=0)] = 0
        return img_hsv, mask
    
    def save_fish_img(self, fish_rect, img_hsv):
        x, y, w, h = fish_rect
        img_rgb = cv2.cvtColor(img_hsv[y:y+h, x:x+w], cv2.COLOR_HSV2BGR)
        cv2.imwrite("Fish.png", img_rgb)
    
    def find_head_and_tail(self, img_hsv):
        img_hsv, mask = self.filter_out_water(img_hsv)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        whole_fish = sorted(contours, key = cv2.contourArea)[-1]
        whole_fish_rectangle = cv2.boundingRect(whole_fish)
        self.save_fish_img(whole_fish_rectangle, img_hsv)
        
        left_contour = sorted(contours, key = cv2.contourArea)[-2]
        left_br = cv2.boundingRect(left_contour)
        right_contour = sorted(contours, key = cv2.contourArea)[-3]
        right_br = cv2.boundingRect(right_contour)
        if left_br[0] > right_br[0]:
            left_br, right_br = right_br, left_br
            
        return left_br, right_br
    
    def find_length(self, left_br, right_br):
        fish_width = left_br[2] + right_br[2]
        elongated_width = right_br[0] + right_br[2] - left_br[0]
        actual_fish_width = 27.94
        scale_factor = actual_fish_width / fish_width
        fish_length = scale_factor*elongated_width + 3.048
        return fish_length
    
    def run(self):
        self.frame_hsv = self.preprocess_image(self.img, self.filter_size)
        self.left, self.right = self.find_head_and_tail(self.frame_hsv)
        return self.find_length(self.left, self.right)
