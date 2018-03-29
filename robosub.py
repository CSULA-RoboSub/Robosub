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
else:
    """Import auv"""
    from modules.main.auv import AUV


class CLI(cmd.Cmd):
    """AUV command line interpreter"""

    intro = '\nType help or ? to list commands.'
    prompt = 'auv> '

    # test #############################################################################################################
    def do_test(self, arg):
        '\n[movement] to test movement\
         \n[cv] to test cv direction finder'

        # if arg.lower() == 'movement':
        #     test_movement.main()

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
        elif arg.lower() == 'set':
            # TODO set tasks
            # AUV.set_config('tasks', '0 1 2 3 4 5 6 7 8')
            print('test')
        elif arg.lower() == 'reset':
            AUV.set_config('tasks', '', True)
        else:
            print(AUV.tasks)

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

    # navigation #######################################################################################################
    def do_navigation(self, arg):
        '\n[cv] toggle computer vision task manager\
         \n[keyboard] keyboard manual navigation\
         \n[x_value y_value z_value rotation_value]:\n\
         \nhorizontal x movement: negative = left, positive = right, 0 = no x movement\
         \nhorizontal y movement: negative = backwards, positive = forwards, 0 = no y movement\
         \nvertical movement: negative = down, positive = up, 0 = no vertical movement\
         \nrotation: negative = left, positive = right, 0 = no rotation'

        if arg.lower() == 'cv' or arg.lower() == 'tm':
            # TODO cv taskmanager
            print(arg)
        elif arg.lower() == 'keyboard' or arg.lower() == 'kb':
            AUV.keyboard_nav()
        elif len(arg.split()) == 4:
            AUV.navigation.navigate(*parse(arg))
        else:
            print('Not a valid navigation argument')

    # auto-complete navigation
    def complete_navigation(self, text, line, start_index, end_index):
        args = ['cv', 'keyboard']

        if text:
            return [arg for arg in args if arg.startswith(text)]
        else:
            return args

    # exit #############################################################################################################
    def do_exit(self, arg):
        '\nExits auv'

        print('Closing Robosub')

        return True


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


if __name__ == '__main__':
    # open roscore in subprocess
    print('Setting up roscore.')
    os.system('killall -9 roscore')
    os.system('killall -9 rosmaster')
    os.system('killall -9 rosout')
    roscore = subprocess.Popen('roscore')
    time.sleep(1)

    AUV = AUV()  # initialize AUV() class

    print('\n***Plug in magnet after setting up configurations to start AUV.***')
    print('\n***Set motor state to 1 to start motors.***')

    AUV.start()  # TESTING PURPOSES ONLY. REMOVE AFTER TESTING (simulates magnet killswitch = 1#############################################################

    CLI().cmdloop()  # run AUV command interpreter

    # close roscore and rosmaster on exit
    subprocess.Popen.kill(roscore)
    os.system('killall -9 rosmaster')
    os.system('killall -9 rosout')
