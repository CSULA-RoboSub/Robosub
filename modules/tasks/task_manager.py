import rospy
import time
import sys
from random import *

from modules.sensors.computer_vision import utils


class TaskManager():
    ''' to decide on the task at hand than send coordinates to navigation'''

    def __init__(self):
        self.coordinates = []
        self.coordinates.append(randint(-1,1))
        self.coordinates.append(randint(-1,1))

    def gate_detect(self):
        print("gate_detect")
        return self.coordinates

    def dice_detect(self):
        print("dice_detect")
        return self.coordinates

    def roulette_detect(self):
        print("roulette_detect")
        return self.coordinates

    def cash_in_detect(self):
        print("cash_in_detect")
        return self.coordinates

    def buoy_detect(self):
        print("buoy_detect")
        return self.coordinates