import utils
import cv2
import numpy as np


class GatePreprocessor:

    def __init__(self):
        self.lower = [0, 180, 55] # would be nice to adjust in cli
        self.upper = [130, 255, 255] # same...
        self.roi_size = 400


    def preprocess(self,  img):
        lower = np.array(self.lower, dtype='uint8')
        upper = np.array(self.upper, dtype='uint8')
        mask = cv2.inRange(img,  lower,  upper)
        output = cv2.bitwise_and(img,  img,  mask=mask)
        return output, mask


    # takes in a list of contours and filters based on upper and lower bound values (length) and returns an np.array
    def filter_contours(img_contours, lower=20, upper=200):
        new_contour_list = []
        for cont in img_contours:
            if len(cont) > lower and len(cont) < upper:
                new_contour_list.append(cont)
        return np.array(new_contour_list)


    def get_interest_regions(self,frame):
        height, width, lines = frame.shape
        center = (width / 2, height / 2)
        pimage, mask = self.preprocess(frame)
        
        imgray = cv2.cvtColor(pimage, cv2.COLOR_BGR2GRAY)
        
        flag, binary_image = cv2.threshold(imgray, 127, 255, cv2.THRESH_TOZERO)
        
        #edges = cv2.Canny(binary_image, 50, 150) # later
        
        im, contours, ret = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours = filter_contours(contours)
        
        boxes = [cv2.boundingRect(c) for c in filtered_contours]
        
        interest_regions = [b for b in boxes if b[2]*b[3] > self.roi_size]
        
        return interest_regions
