import utils
import cv2
import numpy as np


class GatePreprocessor:

    def __init__(self):
        self.lower = [0, 180, 55] # would be nice to adjust in cli
        self.upper = [130, 255, 255] # same...
        self.min_cont_size = 20
        self.max_cont_size = 200
        self.roi_size = 400


    def preprocess(self,  img):
        lower = np.array(self.lower, dtype='uint8')
        upper = np.array(self.upper, dtype='uint8')
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)
        return output, mask


    def get_interest_regions(self, frame):
        height, width, lines = frame.shape
        #center = (width / 2, height / 2) # not used
        pimage, mask = self.preprocess(frame)
        
        imgray = cv2.cvtColor(pimage, cv2.COLOR_BGR2GRAY)
        
        flag, binary_image = cv2.threshold(imgray, 127, 255, cv2.THRESH_TOZERO)
        
        #edges = cv2.Canny(binary_image, 50, 150) # later
        
        im, contours, ret = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # filter the contours based on size
        #print("contours length (before filtering):", len(contours) )
        new_contours_list = []
        for cont in contours:
            if ( (len(cont) > self.min_cont_size) and (len(cont) < self.max_cont_size) ):
                new_contours_list.append(cont)
        filtered_contours = np.array(new_contours_list)
        #print("contours length (AFTER filtering):", len(filtered_contours) )

        boxes = [cv2.boundingRect(c) for c in filtered_contours]
        
        interest_regions = [b for b in boxes if b[2]*b[3] > self.roi_size]
        
        return interest_regions
