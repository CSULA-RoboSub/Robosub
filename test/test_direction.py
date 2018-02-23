import unittest

#import sys
#sys.path.append('../ROS')
from ROS.directionfinder import direct_finder
#from directionfinder import direct_sub

class directTest(unittest.TestCase):
    def test_directions(self):
        '''self.assertEqual(3, math.add(1, 2))
        self.assertEqual(6, math.add(3, 3))'''
        #self.assertEqual(direct_finder.forTravis(3, 4), direct_sub.subTravis())
        self.assertEqual(direct_finder.forTravis(3, 4), [3,4])

    '''def test_multiply_method(self):
        self.assertEqual(6, math.multiply(2, 3))
        self.assertEqual(8, math.multiply(2, 4))
        self.assertEqual(8, math.multiply(4, 2))'''