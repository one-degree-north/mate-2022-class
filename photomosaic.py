import cv2
import numpy as np

class Photomosaic:
    def __init__(self, img_paths):
        self.img_paths = img_paths
        self.num_img = 8
        
    def combine_images(self, img1, img2, dimension):
        width, height = True, False
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        for m in matches:
            if (m[0].distance < 0.5*m[1].distance):
                good.append(m)
        matches = np.asarray(good)
        if (len(matches[:,0]) >= 4):
            src = np.float32([ kp1[m.queryIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
            dst = np.float32([ kp2[m.trainIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
            H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        else:
            raise AssertionError('Can’t find enough keypoints.')

        if dimension is width:
            dst = cv2.warpPerspective(img1, H, ((img1.shape[1] + img2.shape[1]), img2.shape[0]))
            dst[0:img2.shape[0], 0:img2.shape[1]] = img2
            return dst
        elif dimension is height:
            dst = cv2.warpPerspective(img1, H, (img2.shape[1], (img1.shape[0] + img2.shape[0])))
            dst[0:img2.shape[0], 0:img2.shape[1]] = img2
            return dst
        
    def rotate_imgs(self, imgs):
        for i in range(self.num_img/2):
            imgs[i] = cv2.rotate(imgs[i], cv2.cv2.ROTATE_90_CLOCKWISE)
            imgs[7-i] = cv2.rotate(imgs[7-i], cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        return imgs
        
    def run(self):
        width, height = True, False
        self.imgs = [cv2.imread(path) for path in self.img_paths]
        self.imgs = self.rotate_imgs(self.imgs)
        # Combine heights
        # You could set up a divide and conquer algorithm to do the below
        # Use trees and graph algorithms and stuff, but I'm lazy af
        combined_imgs = [self.combine_images(self.imgs[i], self.imgs[7-i], height) for i in range(self.num_img/2)]
        combined_imgs = [
                         self.combine_images(combined_imgs[0], combined_imgs[1], width),
                         self.combine_images(combined_imgs[2], combined_imgs[3], width)
                        ]
        combined_img = self.combine_images(combined_imgs[0], combined_imgs[1], width)
        return combined_img
