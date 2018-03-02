'''Dice task will handle the actual all the individual compenents
which need to be completed to handle the task including which dice need to be searched for'''

import dice_detector as detector
import dice_classifier as classifier
import dice_preprocess as dpp
import Task
class dice_task(Task):

    def __init__(self):
        self.dice_dict = {1: False,2: False,3: False,4: False,5: False,6: False}
        self.found =  False #checking whether or not the dice have been located
        self.complete = False
    def run_task(self):
        while(not self.found):
            found = detector.locate_dice()
        
    def is_task_complete(self):
        return self.complete