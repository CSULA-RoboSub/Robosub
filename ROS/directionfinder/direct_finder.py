import rospy
from random import *
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray

import direct_sub
import time
import sys
sys.path.insert(0, '/home/niivek/Desktop/ros_libraries/openCV')

from taskManager import taskManager

motorNodeIsReady = False
cvNodeIsready = False
startTakingPicture = False
magnetCheck = False

gateComplete = False
diceComplete = False
rouletteComplete = False
cashInCompplete = False
buoyComplete = False
tasksCompleted = False

def check_hardware(statement):
    print('checking hardware...\n')

    global motorNodeIsReady
    global cvNodeIsready
    global startTakingPicture
    global magnetCheck

    motorNodeIsReady = statement
    cvNodeIsready = statement
    startTakingPicture = statement
    magnetCheck = statement

def receiveFromCv(xyCoordinates):
    #the coordinates from CV will be retreived here
    #it will then be appended to xyCoordinates list
    global gateComplete
    global diceComplete
    global rouletteComplete
    global cashInCompplete
    global buoyComplete
    global tasksCompleted

    if not gateComplete:
        gate = taskManager()
        tempcords = gate.gateDetect()
        print(tempcords)
        xyCoordinates.append(tempcords[0])
        xyCoordinates.append(tempcords[1])
        #gateComplete = True

    elif gateComplete and not diceComplete:
        dice = taskManager()
        tempcords = dice.diceDetect()
        print(tempcords)
        xyCoordinates.append(tempcords[0])
        xyCoordinates.append(tempcords[1])
        diceComplete = True

    elif gateComplete and diceComplete and not rouletteComplete:
        roulette = taskManager()
        tempcords = roulette.rouletteDetect()
        print(tempcords)
        xyCoordinates.append(tempcords[0])
        xyCoordinates.append(tempcords[1])
        rouletteComplete = True
    
    elif gateComplete and diceComplete and rouletteComplete and not cashInCompplete:
        cash = taskManager()
        tempcords = cash.cashInDetect()
        print(tempcords)
        xyCoordinates.append(tempcords[0])
        xyCoordinates.append(tempcords[1])
        cashInCompplete = True
    
    elif gateComplete and diceComplete and rouletteComplete and cashInCompplete and not buoyComplete:
        buoy = taskManager()
        tempcords = buoy.buoyDetect()
        print(tempcords)
        xyCoordinates.append(tempcords[0])
        xyCoordinates.append(tempcords[1])
        buoyComplete = True
    
    else:
        print('All tasks have been completed')
        tasksCompleted = True


def direction_finder(xyCoordinates):
    x = xyCoordinates[0]
    y = xyCoordinates[1]

    if x < 0:
        print('move left by {}'.format(x))
        #direct AUV to move to the left by x 
    elif x > 0:
        print('move right by {}'.format(x))
        #direct AUV to move to the right by x 
    else:
        print('hold x position')
        #direct AUV to hold x position
    if y < 0:
        print('move down by {}'.format(y))
        #direct AUV to move up by y
    elif y > 0:
        print('move up by {}'.format(y))
        #direct AUV to move down by y
    else:
        print('hold y position')
        #direct AUV to hold y position
    if x > 0 and y > 0:
        print('Sub must move towards quadrant 1')
    elif x < 0 and y > 0:
        print('Sub must move towards quadrant 2')
    elif x < 0 and y < 0:
        print('Sub must move towards quadrant 3')
    elif x > 0 and y < 0:
        print('Sub must move towards quadrant 4')

    resetVariables(xyCoordinates)

def turn_off_hardware():
    global motorNodeIsReady
    global cvNodeIsready
    global startTakingPicture
    global magnetCheck

    motorNodeIsReady = False
    cvNodeIsready = False
    startTakingPicture = False
    magnetCheck = False

def resetVariables(xyCoordinates):
    xyCoordinates.pop()
    xyCoordinates.pop()

def forTravis(x, y):
    print('x coordinate: {}'.format(x))
    print('y coordinate: {}'.format(y))
    pub_x = rospy.Publisher('x_coordinate', Int32, queue_size=10)
    pub_y = rospy.Publisher('y_coordinate', Int32, queue_size=10)
    pub_both = rospy.Publisher('xy_coordinate', Int32MultiArray, queue_size=10)

    rospy.init_node('direction_node')
    array = []
    array.append(x)
    array.append(y)
    
    pub_array = Int32MultiArray(data=array)

    rospy.loginfo('sending coordinates to ROS')
    pub_x.publish(x)
    pub_y.publish(y)
    pub_both.publish(pub_array)

    return array


def main():
    cvCoordinates = []

    check_hardware(True)

    if magnetCheck:
        print('magnet in place to run mission...')
    if motorNodeIsReady:
        print('motor node is on...')
    if cvNodeIsready:
        print('cv node is on...')
    if startTakingPicture:
        print('picture taking node is on...\n')
    if magnetCheck and motorNodeIsReady and cvNodeIsready and startTakingPicture:
        print('hardware is now active and ready\n')

    pub_x = rospy.Publisher('x_coordinate', Int32, queue_size=10)
    pub_y = rospy.Publisher('y_coordinate', Int32, queue_size=10)
    pub_both = rospy.Publisher('xy_coordinate', Int32MultiArray, queue_size=10)

    rospy.init_node('direction_node')

    #values will need to come in through the CV node
    while not rospy.is_shutdown() and magnetCheck and motorNodeIsReady and cvNodeIsready and startTakingPicture:
        receiveFromCv(cvCoordinates)
        
        if tasksCompleted:
            break

        array = []
        array.append(cvCoordinates[0])
        array.append(cvCoordinates[1])
        
        pub_array = Int32MultiArray(data=array)

        rospy.loginfo('sending coordinates to ROS')
        pub_x.publish(cvCoordinates[0])
        pub_y.publish(cvCoordinates[1])
        pub_both.publish(pub_array)
        
        #direction_finder(cvCoordinates)
        #moved function to direct_sub.py
        #so this will only publish values to ROS
        resetVariables(cvCoordinates)

        print('')
        time.sleep(1)
    
    turn_off_hardware()
    if not magnetCheck and not motorNodeIsReady and not cvNodeIsready and not startTakingPicture:
        print('hardware nodes have now been turned off\n')

if __name__ == "__main__":
    main()