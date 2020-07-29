#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty

class command:

    def __init__(self):
        self._reset = rospy.Publisher('/drone/reset', Empty, queue_size=1)
        self._velocity = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pubLand = rospy.Publisher('/drone/land', Empty, queue_size=1)
        self.pubTakeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.pubReset = rospy.Publisher('/drone/reset', Empty, queue_size=1)
        self.status = 'land'






    def reset(self):
        self._reset.publish(Empty())

    def hover(self):
        self.status = 'hover'
        self._velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))

    def Velocity(self, phi=0, theta=0, gaz=0, yaw=0):
        cmd = Twist()
        cmd.angular.x = 0
        cmd.angular.y = 0
        cmd.angular.z = yaw
        cmd.linear.x = phi
        cmd.linear.y = theta
        cmd.linear.z = gaz
        self.status='vel'
        self._velocity.publish(cmd)





    def SendTakeoff(self):
        # Send a takeoff message to the ardrone driver
        self.status='takeoff'
        self.pubTakeoff.publish(Empty())



    def SendLand(self):
        # Send a landing message to the ardrone driver
        self.status='land'
        self.pubLand.publish(Empty())