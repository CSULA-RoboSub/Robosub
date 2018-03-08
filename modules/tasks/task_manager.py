import rospy
from random import *

from modules.sensors.computer_vision import utils
from modules.control import navigation


class TaskManager():
    """ To decide on the task at hand than send coordinates to navigation"""

    def __init__(self):
    """ To initialize the TaskManger. """
        self.coordinates = []
        n
        #self.is_killswitch_on = navigation.check_kill()

    def gate_detect(self):
    """ When gate_detect task is called. """
    # TODO need to find out which cv node to get coordinates from
        print("gate_detect")
        self.coordinates.append(randint(-1,1))
        self.coordinates.append(randint(-1,1))
        navigation.navigation(self, 1, 1, 1, 1)

    def dice_detect(self):
    """ When dice_detect task is called. """
        print("dice_detect")
        self.coordinates.append(randint(-1,1))
        self.coordinates.append(randint(-1,1))
        navigation.navigation(self, 1, 1, 1, 1)

    def roulette_detect(self):
    """ When roulette_detect task is called. """
        print("roulette_detect")
        self.coordinates.append(randint(-1,1))
        self.coordinates.append(randint(-1,1))
        navigation.navigation(self, 1, 1, 1, 1)

    def cash_in_detect(self):
    """ When cash_in_detect task is called. """
        print("cash_in_detect")
        self.coordinates.append(randint(-1,1))
        self.coordinates.append(randint(-1,1))
        navigation.navigation(self, 1, 1, 1, 1)

    def buoy_detect(self):
    """ When buoy_detect task is called. """
        print("buoy_detect")
        self.coordinates.append(randint(-1,1))
        self.coordinates.append(randint(-1,1))
        navigation.navigation(self, 1, 1, 1, 1)

    def brake(self):
    """ When brake task is called by auv.py. """
        navigation.brake(self)
    
    def start(self):
        """ Starts TaskManager. """
        # TODO perhaps start needs to be call along with which task you would like to perform
        self.navigation.start()
        
    def stop(self):
        """ Stops TasksManager. """
        # TODO can perhaps be used to stop a task when a error/checker is found
        pass
