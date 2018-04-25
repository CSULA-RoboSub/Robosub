import cv2
from sklearn.externals import joblib

class DiceClassifier:

    def __init__(self):
        self.hog = self.get_hog()
        self.dims = (144,144)
        self.lsvm = joblib.load('Dice_SVM_std.pkl')

    '''note that the height and widths must be multiples of 8 in order to use a HOOG'''
    def get_hog(self):
        minDim = 80
        blockSize = (8,8)
        blockStride = (8,8)
        cellSize = (8,8)
        nbins = 9
        derivAperture = 1
        winSigma = -1
        histogramNormType = 0
        L2HysThreshold = 2.1e-1
        gammaCorrection = 0
        nlevels = 64
        dims = (144,144)
        return cv2.HOGDescriptor(dims, blockSize, blockStride, cellSize, nbins, derivAperture, winSigma, histogramNormType, L2HysThreshold, gammaCorrection, nlevels)

    def get_lsvm(self):
        return self.lsvm

    def classify(self,frame,roi): #roi = regions of interest
        die = None
        max = 0
        true_dice = []
        for box in roi:
            x, y, w, h = box
            window = frame[y:y+h, x:x+w, :]
            window = cv2.resize(window, self.dims)
            feat = self.hog.compute(window)
            prob = self.lsvm.predict_proba(feat.reshape(1, -1))[0]
            if prob[1] > .6 and prob[1] > max:
                max = prob[1]
                die = box
        return die