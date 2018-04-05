import rospy
from robosub.msg import Navigate


class Navigation():
    """Controls thrusters to move or point AUV to a certain direction given power and direction or rotational values"""

    def __init__(self, power=0, direction='none', rotation=0.0):
        self.is_killswitch_on = False

        self.directions = {
            'none': 0,
            'forward': 1,
            'right': 2,
            'backward': 3,
            'left': 4,
            'up': 5,
            'down': 6
        }

        self.power = power
        self.direction = direction
        self.rotation = rotation
        # TODO check if submerged

    def set_navigation(self, power=0, direction='none', rotation=0.0):
        """
        power: 0 to 400
        direction: none, forward, right, backward, left, up, down
        rotation: -180.0 to 180.0
        """

        self.power = power
        self.direction = direction
        self.rotation = rotation

    def navigate(self, power, direction, rotation):
        """Start navigation with given power and direction or rotational values."""

        if self.is_killswitch_on:

            if power is not None or direction is not None or rotation is not None:
                self.set_navigation(power, direction, rotation)

            self.pub_navigate(self.power, self.direction, self.rotation)

    def submerge(self, power):
        """ Set the level the sub should submerge to """

        if self.is_killswitch_on:

            print('submerging AUV')
            self.pub_navigate(power, 'down', 0.0)

    def brake(self):
        """ Stops the AUV and propels it the opposite direction to stop momentum"""

        if self.is_killswitch_on:

            opposite_direction = {
                'none': 'none',
                'forward': 'backward',
                'right': 'left',
                'backward': 'forward',
                'left': 'right',
                'up': 'down',
                'down': 'up'
            }

            print('braking AUV')
            self.pub_navigate(self.power, opposite_direction[self.direction], -self.rotation)

    def pub_navigate(self, power, direction, rotation):
        """ Private method used to publish given power, direction, and rotation"""

        pub_navigate = rospy.Publisher('navigation', Navigation)

        navigate = Navigate()
        navigate.power = power
        navigate.direction = self.directions[direction]
        navigate.rotation = rotation

        pub_navigate.publish(navigate)
        rospy.sleep(.1)

        print('moving AUV power=%s, direction=%s, rotation=%d' % (power, direction, rotation))

    def start(self):
        """Starts navigation with set preferences when killswitch is plugged in"""

        self.is_killswitch_on = True
        self.submerge(10)
        # TODO set default submerge value as config file

    def stop(self):
        """Stops navigation when killswitch is unplugged"""

        self.is_killswitch_on = False
