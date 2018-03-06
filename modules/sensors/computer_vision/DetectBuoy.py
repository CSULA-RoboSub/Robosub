import utils
import BuoyClassifier as bc
import cv2
import BuoyPreprocessor as bp


class DetectBuoy:

    def __init__(self):
        self.classifier = bc.BuoyClassifier()
        self.cap = cv2.VideoCapture(0)
        self.preprocess = bp.BuoyPreprocessor()
        self.hog = self.classifier.get_hog()
        self.lsvm = self.classifier.get_lsvm()
        print (self.lsvm)
        self.lower = [0,60,60]
        self.upper = [60,255,255]
        self.coords = (0,0)
        self.isTaskComplete = False
        print self.isTaskComplete

    '''
    def get_directions(self,x,y,w,h):
        return utils.get_directions(x,y,w,h)
    '''
    def detect(self):
        _, frame = self.cap.read()
        height, width, _ = frame.shape
        center = (width / 2, height / 2)
        regions_of_interest = self.preprocess.get_interest_regions(frame)
        '''
        for x, y, w, h in regions_of_interest:
            cv2.rectangle(frame, (x,y), (x+w, y+h), utils.colors["blue"], 2)
        #clone = frame.copy()
        '''
        buoy = self.classifier.classify(frame, regions_of_interest)
        if buoy == None:
            buoy = 100,100,140,280
        x,y,w,h = buoy
        self.coords = utils.get_directions(center, x,y,w,h)

