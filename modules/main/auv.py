import rospy

from std_msgs.msg import Int32
from test import test_movement
from modules.control.motor import Motor
from modules.control.direction import Direction


class AUV():
    """AUV Master, automates tasks"""

    def __init__(self, state=0, tasks=['gate', 'dice', 'slots']):
        self.state = state
        self.tasks = tasks

        # self.test
        self.motor = Motor()  # initialize Motor() class
        # TODO self.cv = CV() # initialize CV() class
        # TODO construct modules, refactor robosub.py

    def start(self):
        """Starts the modules when magnet killswitch is plugged in"""

        self.motor.start()
        # self.cv.start(self.tasks)

    def stop(self):
        """Stops the modules when magnet killswitch is removed"""

        self.motor.stop()
