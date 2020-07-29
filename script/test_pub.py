#!/usr/bin/env python

'''Publish takeoff message'''

from __future__ import print_function
import numpy as np
import cv2, time, math
import rospy
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty, Bool, String
from sensor_msgs.msg import CompressedImage, Imu, Image
from selfiestickdrone.msg import selfie_state
from lib.get_drone_cmd import cmdVel
from geometry_msgs.msg import Twist


def takeoff_sequence(self, seconds_taking_off=1.0):
    # Before taking off, make sure that cmd_vel is not null to avoid drifts.
    self.vel_pub.publish(cmdVel(0, 1))
    self.takeoff_pub.publish(Empty())
    time.sleep(seconds_taking_off)


# Go up and wait for 1 sec
def sendUpCmd(self):
    self.vel_pub.publish(cmdVel(5, 1))
    time.sleep(0.8)
    self.vel_pub.publish(cmdVel(0, 1))
    time.sleep(0.5)


def takeoff_selfie():
    takeoff = False
    selfi = False
    take = rospy.Publisher('/device/takeoff', Bool, queue_size=5)
    sel = rospy.Publisher('/selfie/state', selfie_state, queue_size=10)
    vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
    rospy.init_node('phone_pub', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if not takeoff:
            takeoff = True
            rospy.loginfo(takeoff)
            take.publish(takeoff)
            rospy.sleep(1)
            vel_pub.publish(cmdVel(0, 1))
            time.sleep(0.5)
        elif takeoff and not selfi:
            '''
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  -*- --  --  --  --  --
            --  -- -***---  --  --  --  --
            --  ---*****-- -- -- -- --  --
            --  -- -***---  --  --  --  --
            --  --  -*- --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            --  --  --  --  --  --  --  --
            [Yaw, Centroid_X, Centroid_Y, Bounding Box Ratio]
            '''
            # phone
            #selfie_stat = [-41, 24, 100, 0.1]
            #selfie_stat = [30, 52, 95, 0.12]
            se_st = [0, 320, 180, 0.1]
            rospy.loginfo(se_st)
            sel.publish(se_st)
            selfi = True
        rate.sleep()


if __name__ == '__main__':

    try:
            takeoff_selfie()

    except rospy.ROSInterruptException:
        pass