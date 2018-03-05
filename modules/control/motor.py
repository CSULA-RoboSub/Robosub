import rospy
from std_msgs.msg import Int32
from time import sleep


class Motor():
    """Controls motors"""

    def __init__(self, state=0):
        self.is_killswitch_on = False

        self.state = state

        def callback(data):
            self.state = data.data

        rospy.Subscriber('motor_state', Int32, callback)

    def get_state(self):
        return self.state

    def toggle_state(self, arg=None):
        """Toggles the state of the motors (1 == on, 0 == off, empty == toggle)"""

        # Toggles the state if there is no argument passed
        if arg is None:
            if self.state == 0:
                self.state = 1
            else:
                self.state = 0
        else:
            self.state = arg

        print('\nmotor state set to %d' % self.state)

    def move(self, y):
        """Propel AUV forward or backwards with given y value
        positive = forwards, negative = backwards
        """

        if self.is_killswitch_on:
            pub = rospy.Publisher('move', Int32, queue_size=10)

            pub.publish(y)
            sleep(.2)

    def start(self):
        """Starts motors with set preferences when killswitch is plugged in"""

        self.is_killswitch_on = True

        pub = rospy.Publisher('motor_state', Int32, queue_size=10)

        pub.publish(self.state)
        sleep(.2)

        print('\nmotor state published %d' % self.state)

    def stop(self):
        """Stops motors when killswitch is unplugged"""

        self.is_killswitch_on = False

        pub = rospy.Publisher('motor_state', Int32, queue_size=10)

        pub.publish(0)
        sleep(.2)
