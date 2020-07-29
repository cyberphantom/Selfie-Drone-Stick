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

    elif action == 9:  # Forward + Tilt Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 10:  # Forward + Tilt Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 11:  # Forward + Up
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 12:  # Forward + Down
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 13:  # Forward + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 14:  # Forward + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 15:  # Backword + Tilt Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 16:  # Backword + Tilt Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = 0.0

    elif action == 17:  # Backword + Up
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 18:  # Backword + Down
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 19:  # Backword + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 20:  # Backword + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 21:  # Tilt Left + Up
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 22:  # Tilt Left + Down
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 23:  # Tilt Left + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 24:  # Tilt Left + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 25:  # Tilt Right + Up
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 26:  # Tilt Right + Down
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 27:  # Tilt Right + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 28:  # Tilt Right + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 29:  # Up + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 30:  # Up + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 31:  # Down + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 32:  # Down + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 33:  # Forward + Tilt Left + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 34:  # Forward + Tilt Left + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 35:  # Forward + Tilt Right + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 36:  # Forward + Tilt Right + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 37:  # Forward + Tilt Left + Up
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 38:  # Forward + Tilt Left + Down
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 39:  # Forward + Tilt Right + Up
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 40:  # Forward + Tilt Right + Down
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 41:  # Forward + Up + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 42:  # Forward + Up + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 43:  # Forward + Down + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 44:  # Forward + Down + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 45:  # Backword + Tilt Left + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 46:  # Backword + Tilt Left + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 47:  # Backword + Tilt Right + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = vel

    elif action == 48:  # Backword + Tilt Right + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.z = -vel

    elif action == 49:  # Backword + Tilt Left + Up
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 50:  # Backword + Tilt Left + Down
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 51:  # Backword + Tilt Right + Up
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = 0.0

    elif action == 52:  # Backword + Tilt Right + Down
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = 0.0

    elif action == 53:  # Backword + Up + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 54:  # Backword + Up + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 55:  # Backword + Down + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 56:  # Backword + Down + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 57:  # Tilt Left + Up + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 58:  # Tilt Left + Up + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 59:  # Tilt Left + Down + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 60:  # Tilt Left + Down + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 61:  # Tilt Right + Up + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 62:  # Tilt Right + Up + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 63:  # Tilt Right + Down + Ang Left
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 64:  # Tilt Right + Down + Ang Right
        vel_cmd.linear.x = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 65:  # Forward + Down + Tilt Left + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 66:  # Forward + Down + Tilt Left + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 67:  # Forward + Down + Tilt Right + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 68:  # Forward + Down + Tilt Right + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 69:  # Forward + Up + Tilt Left + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 70:  # Forward + Up + Tilt Left + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 71:  # Forward + Up + Tilt Right + Ang Left
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 72:  # Forward + Up + Tilt Right + Ang Right
        vel_cmd.linear.x = vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 73:  # Backword + Down + Tilt Left + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 74:  # Backword + Down + Tilt Left + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 75:  # Backword + Down + Tilt Right + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = vel

    elif action == 76:  # Backword + Down + Tilt Right + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = -vel
        vel_cmd.angular.z = -vel

    elif action == 77:  # Backword + Up + Tilt Left + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 78:  # Backword + Up + Tilt Left + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    elif action == 79:  # Backword + Up + Tilt Right + Ang Left
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = vel

    elif action == 80:  # Backword + Up + Tilt Right + Ang Right
        vel_cmd.linear.x = -vel
        vel_cmd.angular.x = 0.0
        vel_cmd.linear.y = -vel
        vel_cmd.angular.y = 0.0
        vel_cmd.linear.z = vel
        vel_cmd.angular.z = -vel

    return vel_cmd