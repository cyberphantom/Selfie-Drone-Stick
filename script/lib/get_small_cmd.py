#!/usr/bin/env python

from geometry_msgs.msg import Twist

def cmdVel(ac, vel):
    vel_cmd = Twist()
    action = ac
    if action == 0:  # Hover
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    if action == 1:  # Forward
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 2:  # Backword
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 3:  # Tilt Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 4:  # Tilt Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 5:  # Up
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 6:  # Down
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 7:  # Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 8:  # Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    return vel_cmd
