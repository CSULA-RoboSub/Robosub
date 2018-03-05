import rospy
from std_msgs.msg import Int32
from time import sleep


class Direction():
    """Controls thrusters to point AUV to a certain direction given rotation and z values
    rotation: negative = left, positive = right, 0 = no rotation
    vertical movement: negative = down, positive = up, 0 = no vertical movement
    """

    def __init__(self, rotation=0, z=0):
        self.is_killswitch_on = False

        # rotation: negative = left, positive = right, 0 = no rotation
        self.rotation = rotation
        # vertical movement: negative = down, positive = up, 0 = no vertical movement
        self.z = z

    def set_direction(self, rotation=0, z=0):
        self.rotation = rotation
        self.z = z

    def point_direction(self):
        """Points AUV to direction with given rotation and z values"""

        if self.is_killswitch_on:

            pub_rotation = rospy.Publisher('rotation_direction', Int32, queue_size=10)

            pub_vertical = rospy.Publisher('vertical_direction', Int32, queue_size=10)

            pub_rotation.publish(self.rotation)
            pub_vertical.publish(self.z)
            sleep(.2)

            print('moving AUV to rotation=%d, z=%d' % (self.rotation, self.z))

    def start(self):
        """Starts direction with set preferences when killswitch is plugged in"""

        self.is_killswitch_on = True

    def stop(self):
        """Stops direction when killswitch is unplugged"""

        self.is_killswitch_on = False
