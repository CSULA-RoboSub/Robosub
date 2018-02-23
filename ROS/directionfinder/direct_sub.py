import rospy
from std_msgs.msg import Int32MultiArray

def directions(data):
    rospy.loginfo('Receiving coordinates from ROS')
    coordinates = data.data
    x = coordinates[0]
    y = coordinates[1]

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
    print('')


def get_coords():
    rospy.init_node('get_coords', anonymous=True)
    rospy.Subscriber('xy_coordinate', Int32MultiArray, directions)
    rospy.spin()

if __name__ == '__main__':
    get_coords()
