import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Int8MultiArray


class Navigation():
    """Controls thrusters to move or point AUV to a certain direction given x, y, z, or rotational values
    horizontal x movement: negative = left, positive = right, 0 = no x movement
    horizontal y movement: negative = backwards, positive = forwards, 0 = no y movement
    vertical movement: negative = down, positive = up, 0 = no vertical movement
    rotation: negative = left, positive = right, 0 = no rotation
    """

    def __init__(self, x=0, y=0, z=0, rotation=0.0):
        self.is_killswitch_on = False

        # horizontal x movement: negative = left, positive = right, 0 = no  x movement
        self.x = x

        # horizontal y movement: negative = backwards, positive = forwards, 0 = no y movement
        self.y = y

        # vertical movement: negative = down, positive = up, 0 = no vertical movement
        self.z = z

        # rotation: negative = left, positive = right, 0 = no rotation
        self.rotation = rotation

    def set_navigation(self, x=0, y=0, z=0, rotation=0.0):
        """
        horizontal x movement: negative = left, positive = right, 0 = no x movement
        horizontal y movement: negative = backwards, positive = forwards, 0 = no y movement
        vertical movement: negative = down, positive = up, 0 = no vertical movement
        rotation: negative = left, positive = right, 0 = no rotation
        """

        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation

    def navigate(self, x, y, z, rotation):
        """ Start navigation with given x, y, z, rotation values."""

        if self.is_killswitch_on:

            if x is not None or y is not None or z is not None or rotation is not None:
                self.set_navigation(x, y, z, rotation)

            self.pub_navigate(self.x, self.y, self.z, self.rotation)

    def submerge(self, z):
        """ Set the level the sub should submerge to """

        if self.is_killswitch_on:

            print('submerging AUV')
            self.pub_navigate(0, 0, z, 0.0)

    def brake(self):
        """ Stops the AUV and propels it the opposite y value to stop momentum"""

        if self.is_killswitch_on:

            print('braking AUV')
            self.pub_navigate(0, -self.y, 0, 0.0)

    def pub_navigate(self, x, y, z, rotation):
        """ Private method used to publish given x, y, z, rotation"""

        navigate = Int8MultiArray(data=[x, y, z])
        pub_navigate = rospy.Publisher('navigation', Int8MultiArray, queue_size=10)
        pub_rotation = rospy.Publisher('rotation', Float32, queue_size=10)

        pub_navigate.publish(navigate)
        pub_rotation.publish(rotation)
        rospy.sleep(.1)

        print('moving AUV to x=%d, y=%d, z=%d, rotation=%d' % (x, y, z, rotation))

    def start(self):
        """Starts navigation with set preferences when killswitch is plugged in"""

        self.is_killswitch_on = True
        self.submerge(-5)
        # TODO set default submerge value as config file

    def stop(self):
        """Stops navigation when killswitch is unplugged"""

        self.is_killswitch_on = False
