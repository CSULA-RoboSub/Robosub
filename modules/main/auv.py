import rospy
from std_msgs.msg import Int8

# from test import test_movement
from modules.control.motor import Motor
from modules.control.navigation import Navigation


class AUV():
    """AUV Master, automates tasks"""

    def __init__(self, state=0, tasks=['gate', 'dice', 'slots']):
        rospy.init_node('AUV', anonymous=True)  # initialize AUV rosnode

        def callback(data):
            if data.data == 1:
                self.start()
            if data.data == 0:
                self.stop()

        rospy.Subscriber('kill_switch', Int8, callback)  # Subscriber for magnet kill switch

        self.state = state
        self.tasks = tasks

        # self.test
        self.motor = Motor()  # initialize Motor() class
        self.navigation = Navigation()  # initialize Navigation() class
        # TODO self.cv = CV() # initialize CV() class
        # TODO construct modules, refactor robosub.py

    def start(self):
        """Starts the modules when magnet killswitch is plugged in"""

        self.motor.start()
        self.navigation.start()
        # self.cv.start(self.tasks)

    def stop(self):
        """Stops the modules when magnet killswitch is removed"""

        self.motor.stop()
