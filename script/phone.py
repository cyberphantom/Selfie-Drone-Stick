#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import cv2, time, math
import rospy, rospkg
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty, UInt8, String
from sensor_msgs.msg import CompressedImage, Imu, Image
from selfiestickdrone.msg import device_state, selfie_state

from face_human_detection_tracking_agent.face_det import detect_face

from lib.helper import *

# Set the logging system
rospack = rospkg.RosPack()
pkg_path = rospack.get_path('Selfie-Drone-Stick')

class phone_IO:

    '''face detection'''
    fd = detect_face()

    selfie = False

    def __init__(self):
        self.bridge = CvBridge()

        self.imu = None
        self.gyro = None
        self.pre = None
        self.rotation = [None, None, None]
        self.x = None
        self.drone_state = rospy.get_param("/drone_state/idle")
        self.land = True
        self.shoot = None
        self.device_img = rospy.Publisher("/device/image_raw", Image, queue_size=1)
        self.device_signal = rospy.Publisher("/device/signal", UInt8, queue_size=5)
        self.device_selfie = rospy.Publisher("/device/selfie", device_state, queue_size=10)
        self.sstate = rospy.Publisher("/selfie/state", selfie_state, queue_size=10)


    # Define Subscribers
    def phone_subscriber(self):

        # device images and IMU
        rospy.Subscriber("/device/img", CompressedImage, self.callback)

        rospy.Subscriber("/device/imu", Imu, self.imuCallback)

        rospy.Subscriber("/device/gyro", Imu, self.gyroCallback)

        rospy.Subscriber("/device/pre", Imu, self.preCallback)

        rospy.Subscriber("/selfie/shoot", String, self.shootCallback)



    def callback(self, _image):
        box_ratio = None
        box_centroid = None

        ''' Convert CompressedImage to np '''
        np_arr = np.fromstring(_image.data, np.uint8)

        ''' Convert np array to cv image '''
        image_cv = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #print(image_cv.shape[:2])

        ''' Resize the Image '''
        _frame = cv2.resize(image_cv, (120, 150))
        #enlarge = cv2.resize(self._frame, (120*3, 150*3))
        ready_image = _frame.copy()

        '''Call detection, box = [x_min(int),y_min(int,x_max(int),y_max(int)]'''
        detected_image, box = self.fd.run_detect(ready_image)

        #Done!


        ''' Publishing the resulted frame '''
        #self.phone_img.publish(self.bridge.cv2_to_imgmsg(tracked_image, "bgr8"))

        if box is not None:
            h, w, _ = _frame.shape
            box_ratio, box_centroid = bounding_box(w, h, box)


        if (self.x is not None and self.rotation[0] is not None and self.rotation[1] is not None and self.rotation[2] is not None):

            '''taking off 
            only when self.takeoff = False
            To take off self.x = self.rotations = 0
            '''
            if ((abs(abs(self.x) - 90)<= 2) and (abs(self.rotation[0]) <= 3) and (abs(self.rotation[1]) <= 5) and (abs(self.rotation[2])) <= 5):
                if self.drone_state == rospy.get_param("/drone_state/idle"):
                    self.drone_state = rospy.get_param("/drone_state/take_off")
                    self.device_signal.publish(self.drone_state)
                    self.land = False


            '''landing'''
            if ((abs(self.x) >= 178) and (abs(self.rotation[0]) <= 3) and (abs(self.rotation[1]) >= 84) and (abs(self.rotation[2]) <= 5)):
                if self.takeoff:
                    self.takeoff = False
                    self.land = True
                    self.phone_takeoff.publish(self.takeoff)


            '''Publishing to front user'''
            self.dstate.publish([self.x, self.rotation[0], self.rotation[1], self.rotation[2]])



            ''' Generate state '''
            if box[0] > 0 and box[1] > 0 and box[2] <= 120 and box[3] <= 150 and box_ratio:
                '''box_ratio valid only between 0.1 and 0.2'''
                if box_ratio <= 0.2 or box_ratio >= 0.1:
                    '''[yaw angle, centriod.x for roll, centriod.y for alt correction, box ratio for depth to pitch]'''
                    selfie_stat = [self.rotation[2], box_centroid[0], box_centroid[1], box_ratio]
                    #print(selfie_stat)
                    if self.shoot is not None:
                        self.sstate.publish(selfie_stat)
                        outdir = pkg_path + '/selfie'
                        cv2.imwrite(os.path.join(outdir, 'selfie.png'), ready_image)
                        self.shoot = None



        '''testing'''
        cv2.imshow("base-image", detected_image)
        cv2.waitKey(3)

    '''original imu'''
    def imuCallback(self, _imu):
        self.imu = _imu



    '''fused gyro - get x'''
    def gyroCallback(self, _gyro):
        x, y, z= quaternion_to_euler_angle(_gyro.orientation.x, _gyro.orientation.y, _gyro.orientation.z, _gyro.orientation.w)
        self.rotation[1] = x #arround y axis from 0 to 90 +ve when front facing ground


    '''fused predected - get x and z rotation'''
    def preCallback(self, _pre):
        self.x, y, z = quaternion_to_euler_angle(_pre.orientation.x, _pre.orientation.y, _pre.orientation.z, _pre.orientation.w)

        '''x should be arround 90 to take off'''
        self.rotation[2] = z #arround z axis -ve to the left +ve to the right -60 ---- 60
        self.rotation[0] = y #arround x axis +ve to left -ve to the right


    def shootCallback(self, data):
        self.shoot = data.data
        print(self.shoot)





