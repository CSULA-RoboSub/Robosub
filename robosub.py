"""Import line-oriented command interpreter"""
import cmd
import subprocess
import time
import os

"""If ROS is not detected, installs ROS lunar for Ubuntu 17.04."""
try:
    import rospy
except ImportError:
    import sys
    from scripts import setup_ros

    print('No ROS detected')
    response = raw_input(
                '\nAre you sure you want to do first time setup for ROS? [y/n]: '
            ).lower()
    if response == 'y':
        print('Setting up ROS lunar for Ubuntu 17.04')
        setup_ros.install()

    sys.exit()
finally:
    from std_msgs.msg import Int32

    """Import auv"""
    from modules.main.auv import AUV

    # """Import test_movement"""
    # from test import test_movement

    # """Import motor"""
    # from modules.control.motor import Motor

    # """Import direction"""
    # from modules.control.direction import Direction


class CLI(cmd.Cmd):
    """AUV command line interpreter"""

    intro = '\nType help or ? to list commands.'
    prompt = 'auv> '

    # test #############################################################################################################
    def do_test(self, arg):
        '\n[movement] to test movement\
         \n[cv] to test cv direction finder'

        if arg.lower() == 'movement':
            test_movement.main()

        # TODO finish test

    # auto-complete test
    def complete_test(self, text, line, start_index, end_index):
        args = ['movement', 'cv']

        if text:
            return [arg for arg in args if arg.startswith(text)]
        else:
            return args

    # tasks ############################################################################################################
    def do_tasks(self, arg):
        '\n[view] to view tasks\
         \n[set] to set tasks list\
         \n[reset] to reset tasks list'

        if arg.lower() == 'view':
            print(AUV.tasks)
        elif arg.lower() == 'reset':
            AUV.tasks = ['test', 'fdsdfdsf']

        # TODO set tasks and reset tasks
        # TODO make a config file for default tasks

    # auto-complete tasks
    def complete_tasks(self, text, line, start_index, end_index):
        args = ['view', 'set', 'reset']

        if text:
            return [arg for arg in args if arg.startswith(text)]
        else:
            return args

    # motor ############################################################################################################
    def do_motor(self, arg):
        '\nTurn on or off motors [on/off] or [1/0]\
         \n[toggle] to toggle the current state\
         \n[state] or no argument to print current state'

        if arg.lower() == 'on' or arg == '1':
            AUV.motor.toggle_state(1)
        elif arg.lower() == 'off' or arg == '0':
            AUV.motor.toggle_state(0)
        elif arg.lower() == 'toggle':
            AUV.motor.toggle_state()
        else:
            print('\nmotor state: %d' % AUV.motor.get_state())

    # auto-complete motor
    def complete_motor(self, text, line, start_index, end_index):
        args = ['on', 'off', 'toggle', 'state']

        if text:
            return [arg for arg in args if arg.startswith(text)]
        else:
            return args

    # direction ########################################################################################################
    def do_direction(self, arg):
        '\n[cv] toogle computer vision direction finder\
         \n[rotation# vertical#] negative# = left/down, positive# = right/up'

        if arg.lower() == 'cv':
            print(arg)
        elif len(arg.split()) == 2:
            AUV.direction.set_direction(*parse(arg))
            AUV.direction.point_direction()

    # auto-complete direction
    def complete_direction(self, text, line, start_index, end_index):
        args = ['cv']

        if text:
            return [arg for arg in args if arg.startswith(text)]
        else:
            return args

    # exit #############################################################################################################
    def do_exit(self, arg):
        '\nExits auv'

        return True


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


def callback(data):
    # print(data.data)
    if data.data == 1:
        AUV.start()
    if data.data == 0:
        AUV.stop()


if __name__ == '__main__':
    # open roscore in subprocess
    print('Setting up roscore.')
    os.system('killall -9 roscore')
    os.system('killall -9 rosmaster')
    os.system('killall -9 rosout')
    roscore = subprocess.Popen('roscore')
    time.sleep(1)

    rospy.init_node('AUV', anonymous=True)  # initialize AUV rosnode
    AUV = AUV()  # initialize AUV() class

    print('\n***Plug in magnet after setting up configurations to start AUV.***')

    CLI().cmdloop()  # run AUV command interpreter

    rospy.Subscriber('kill_switch', Int32, callback)  # Subscriber for magnet kill switch

    # close roscore and rosmaster on exit
    subprocess.Popen.kill(roscore)
    os.system('killall -9 rosmaster')
    os.system('killall -9 rosout')
