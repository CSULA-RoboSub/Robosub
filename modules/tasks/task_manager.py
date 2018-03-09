import rospy
from random import *
from std_msgs.msg import Int32MultiArray

from modules.sensors.computer_vision import DetectBuoy
from modules.sensors.computer_vision import DiceDetector
from modules.control.navigation import Navigation


class TaskManager():
    """ To decide on the task at hand than send coordinates to navigation"""

    def __init__(self):
        """ To initialize the TaskManger. """

        self.coordinates = []
        self.navigation = Navigation()
        #rospy.init_node('task_manager')
        #self.is_killswitch_on = navigation.check_kill()

    def detect_gate(self):
        """ When gate_detect task is called. """

    # TODO need to find out which cv node to get coordinates from
        print("detect_gate")
        #self.coordinates.append(randint(-1,1))
        #self.coordinates.append(randint(-1,1))
        #self.navigation.nagivate(1, 1, 1, 1)

    def detect_dice(self):
        """ When dice_detect task is called. """
        """ calls DiceDetector module and creates an instance """
        """ then gets the coordinates of the dice in the pool """
        """ putting coordinates in dice_coordinates """
        """ sends coordinates to navigation module """

        print("detect_dice")
        detectdice = DiceDetector()
        #self.coordinates.append(randint(-1,1))
        #self.coordinates.append(randint(-1,1))
        dice_coordinates = detectdice.locate_dice()
        self.navigation.nagivate(dice_coordinates)

    def detect_roulette(self):
        """ When roulette_detect task is called. """

        print("detect_roulette")
        #self.coordinates.append(randint(-1,1))
        #self.coordinates.append(randint(-1,1))
        #self.navigation.nagivate(1, 1, 1, 1)

    def detect_cash_in(self):
        """ When cash_in_detect task is called. """

        print("detect_cash_in")
        #self.coordinates.append(randint(-1,1))
        #self.coordinates.append(randint(-1,1))
        #self.navigation.nagivate(1, 1, 1, 1)

    def detect_buoy(self):
        """ When detect_buoy task is called. """
        """ Once called, will retreive coordinates from ROS with subscriber """
        """ Then will send coordinates to Navigation module """
        """ Sub will navigate towards listed coordinates """

        # included 2 mothods to broadcast coordinates
        # could broadcast through ROS or be called by the module name

        """ This is the portion that must be sent back to HOUSTON """
        """ We are calling DetectBuoy to detect the buoy in the pool """
        """ Then sending the coordinates back to HOUSTON """
        """ which will be sent from HOUSTON to NAVIGATION """
        """ ********************************************* """
        print("detect_buoy")
        detectbuoy = DetectBuoy()
        buoy_coordinates = detectbuoy.detect()

        # TODO send coordinates to Houston


        self.navigation.nagivate(buoy_coordinates)

        '''pub_task = rospy.Publisher('coordinates', Int32MultiArray, queue_size=10)
        pub_array = Int32MultiArray(data=buoy_coordinates)

        rospy.loginfo('sending coordinates to ROS')
        pub_task.publish(pub_array)

        rospy.init_node('buoy_coordinates', anonymous=True)
        rospy.Subscriber('xy_coordinate', Int32MultiArray, directions)'''

    def direction(data):
        """ Directions is called upon after rospy.subscriber to obtain value from ROS """

        rospy.loginfo('Receiving coordinates from buoy_coordinates')
        coordinates = data.data
        self.navigation.navigate(coordinates)

    def brake(self):
        """ When brake task is called by auv.py. """

        navigation.brake(self)
    
    def start(self):
        """ Starts TaskManager. """

        # TODO perhaps start needs to be call along with which task you would like to perform
        self.navigation.start()
        
    def stop(self):
        """ Stops TasksManager. """
        rospy.on_shutdown(shutdown())
        # TODO can perhaps be used to stop a task when a error/checker is found
        pass

    def shutdown():
        """ Shutdown message for TaskManager """

        print('Shutting down Taskmanager')
