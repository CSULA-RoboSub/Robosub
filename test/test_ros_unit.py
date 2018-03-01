
PKG = 'simple_unittest'

import sys
import unittest

from ROS.directionfinder import direct_finder

print('ROS_unittest')
print()

class TestingDirections(unittest.TestCase):
    def test_direction_input(self):
        print('testing directions')
        self.assertEquals(1, 1, "1!=1")
        self.assertEqual(direct_finder.forUnit(3, 4), [3,4])
        self.assertEqual(direct_finder.forUnit(1, 10),[1,10])
    
class TestingOthers(unittest.TestCase):
    def test_other_functions(self):
        print('testing others')
        self.assertEquals(1, 1, "1!=1")

class TestingMisc(unittest.TestCase):
    def test_misc(self):
        print('testing misc')
        self.assertNotEqual(1, 0)
        self.assertEquals(1, 1+0, 2-1)

if __name__ == '__main__':
    import rostest
    rostest.rosrun(PKG, 'test_directions', TestingDirections)
    rostest.rosrun(PKG, 'test_other_funtions', TestingOthers)
    rostest.rosrun(PKG, 'test_misc', TestingMisc)