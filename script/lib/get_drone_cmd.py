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

    elif action == 2:  # Forward + Tilt Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 3:  # Forward + Tilt Left + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 4:  # Forward + Tilt Left + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 5:  # Forward + Tilt Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 6:  # Forward + Tilt Right + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 7:  # Forward + Tilt Right + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 8:  # Forward + Up
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 9:  # Forward + Down
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 10:  # Forward + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 11:  # Forward + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 12:  # Forward + Tilt Left + Up
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 13:  # Forward + Tilt Left + Down
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 14:  # Forward + Tilt Right + Up
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 15:  # Forward + Tilt Right + Down
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 16:  # Forward + Up + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 17:  # Forward + Up + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 18:  # Forward + Down + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 19:  # Forward + Down + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 20:  # Backword
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 21:  # Backword + Tilt Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 22:  # Backword + Tilt Left + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 23:  # Backword + Tilt Left + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 24:  # Backword + Tilt Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 25:  # Backword + Tilt Right + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 26:  # Backword + Tilt Right + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 27:  # Backword + Up
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 28:  # Backword + Down
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 29:  # Backword + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 30:  # Backword + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 31:  # Backword + Tilt Left + Up
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 32:  # Backword + Tilt Left + Down
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 33:  # Backword + Tilt Right + Up
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 34:  # Backword + Tilt Right + Down
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 35:  # Backword + Up + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 36:  # Backword + Up + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 37:  # Backword + Down + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 38:  # Backword + Down + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 39:  # Tilt Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 40:  # Tilt Left + Up
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 41:  # Tilt Left + Down
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 42:  # Tilt Left + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 43:  # Tilt Left + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 44:  # Tilt Left + Up + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 45:  # Tilt Left + Up + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 46:  # Tilt Left + Down + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 47:  # Tilt Left + Down + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 48:  # Tilt Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 49:  # Tilt Right + Up
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 50:  # Tilt Right + Down
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 51:  # Tilt Right + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 52:  # Tilt Right + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 53:  # Tilt Right + Up + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 54:  # Tilt Right + Up + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 55:  # Tilt Right + Down + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 56:  # Tilt Right + Down + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 57:  # Up
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 58:  # Down
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 59:  # Up + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 60:  # Down + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel


    elif action == 61:  # Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 62:  # Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    return vel_cmd