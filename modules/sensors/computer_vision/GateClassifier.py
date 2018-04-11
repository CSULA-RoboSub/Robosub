import cv2
import glob
import numpy as np
import pandas as pd
import utils as ut
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import Classifier

class GateClassifier:

    def __init__(self):
        self.min_dim = 80
        self.block_size = (16, 16)
        self.block_stride = (8, 8)
        self.cell_size = (8, 8)
        self.bins = 9
        self.dims = (80, 80)
        self.hog = None # init in first-time method call
        self.lsvm = None # init in first-time method call


    def get_hog(self):
        if (self.hog == None):
            self.hog = cv2.HOGDescriptor(
                self.dims,
                self.block_size,
                self.block_stride,
                self.cell_size,
                self.bins,
            )
        return self.hog
            

    def get_features_with_label(self, img_data, label):
        data = []
        for img in img_data:
            img = cv2.resize(img, self.dims)
            feat = self.hog.compute(img[:, :, :3] )
            data.append((feat, label))
        return data

    def get_lsvm(self):
        if (self.lsvm == None):
            pos_imgs = []
            neg_imgs = []
            for img in glob.glob('data/gate/positive/*.jpg'):
                n = cv2.imread(img)
                pos_imgs.append(n)
            for img in glob.glob('data/gate/negative/*.jpg'):
                n = cv2.imread(img)
                neg_imgs.append(n)
            positive_data = self.get_features_with_label(pos_imgs, 1)
            negative_data = self.get_features_with_label(neg_imgs, 0)

            data = positive_data + negative_data

            np.random.shuffle(data) # use np instead

            feat, labels = map(list, zip(*data) )
            feat_flat = [x.flatten() for x in feat]

            features_df = pd.DataFrame(feat_flat)
            labels_df = pd.Series(labels)

            feat_train, feat_test, label_train, label_test = train_test_split(
                features_df,
                labels_df,
                test_size=0.3,
                random_state=2
            )

            self.lsvm = SVC(kernel="linear", C = 1.0, probability=True, random_state=2)
            self.lsvm.fit(feat_train, label_train)
            
            result = self.lsvm.predict(feat_test) # ?

        return self.lsvm

    
    '''
        this returns the max value for the GATE, (x,y) as topleft corner
        then w,h and width and height respectively.
    '''
    def classify(self, frame, roi): #roi = regions of interest
        gate = None
        max_val = 0
        for box in roi:
            x, y, w, h = box
            window = frame[y:y + h, x:x + w, :]
            window_resized = cv2.resize(window, self.dims)
            feat = self.hog.compute(window_resized)
            prob = self.lsvm.predict_proba( feat.reshape(1, -1) )[0]
            if prob[1] > .1 and prob[1] > max_val:
                gate = box
        return gate
