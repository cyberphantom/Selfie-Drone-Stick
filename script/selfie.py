#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import rospy

from cv_bridge import CvBridge, CvBridgeError

from phone import phone_IO
from drone import drone_IO



if __name__ == '__main__':

    ''' After Starting the ARDrone, We start getting Images from the Phone'''

    rospy.init_node('ucf_selfiestick_drone', anonymous=True)

    dio = drone_IO()
    phio = phone_IO()


    try:
        phio.phone_subscriber()
        dio.drone_subscriber()

        rospy.spin()

        if rospy.is_shutdown():
            dio.co.SendLand()
            dio.co.SendLand()

    except CvBridgeError as e:
        print(e)

    except KeyboardInterrupt:
        print("Shutting down")

    except rospy.ROSInterruptException:
        pass
