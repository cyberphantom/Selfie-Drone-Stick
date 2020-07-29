#!/usr/bin/env python
from __future__ import print_function
import cv2, time
import rospy
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty, Bool
from sensor_msgs.msg import CompressedImage, Image
from geometry_msgs.msg import Twist, Pose
from selfiestickdrone.msg import device_state, selfie_state, sds

#from face_human_detection_tracking_agent.humanDT import dronet_detect
from face_human_detection_tracking_agent.dunet.droset_person_od import person_detector

from control_agent.controlAgent import controller
from control_agent.commands_agent.commandsAgent import command

from lib.helper import *


class drone_IO:

  '''human detection'''
  pd = person_detector()
  co = command()

  def __init__(self):
    self.bridge = CvBridge()
    self.controller = controller()
    self.command = command()

    self.drone_rotation = [None, None, None]
    self.drone_frame = None
    self.box = None
    self.box_centroid = None
    self.box_ratio = None

    '''Initialize drone status'''
    self.drone_status = rospy.get_param("/drone_state/idle")

    # self.image_pub = rospy.Publisher("/ucf_drone/image_raw", Image, queue_size=10)

    # Publish the drone observations
    self.sds_state = rospy.Publisher("/sds/state", sds, queue_size=3)

    self.twist = Twist()

    self.selfie = None
    self.stick = None

    self.SDS = sds()


  # Define Subscribers
  def drone_subscriber(self):
      print('Start Drone Subscribing################################################')

      rospy.Subscriber("/device/takeoff", Bool, self.deviceTakeoff_callback)

      '''Subscribe to frontal image'''
      rospy.Subscriber("/drone/front_camera/image_raw",Image, self.callback)

      '''Subscribe to drone IMU'''
      rospy.Subscriber("/drone/gt_pose", Pose, self.imu_callback)
      #rospy.Subscriber("/drone/gt_pose", Pose, self.imu_callback)

      '''Subscribe to selfie data'''
      rospy.Subscriber("/selfie/state", selfie_state, self.selfie_callback)

      '''Subscribe to sds data'''
      rospy.Subscriber("/sds/state", sds, self.selfie_callback)


  def deviceTakeoff_callback(self, bo):
      if bo.data and self.drone_status == 'land':
          self.co.SendTakeoff()
          rospy.sleep(3)
          self.drone_status = 'deviceTakeoff'



  def imu_callback(self, _imu):
      x, y, z = quaternion_to_euler_angle(_imu.orientation.x, _imu.orientation.y, _imu.orientation.z,
                                                      _imu.orientation.w)
      self.drone_rotation[0] = x
      self.drone_rotation[1] = y
      self.drone_rotation[2] = z


  def selfie_callback(self, _selfie):
      self.selfie = _selfie.selfiestate


  def callback(self, data):

    _frame = self.bridge.imgmsg_to_cv2(data, "bgr8")

    ready_image = _frame.copy()

    '''Call detection, box = [x_min(int),y_min(int,x_max(int),y_max(int)]'''
    #detected_image, self.box = self.pd.run_detect(ready_image)
    self.box, self.box_ratio, self.box_centroid = self.pd.run_detect(ready_image)

    try:

        if self.drone_status != 'land':

            if self.drone_rotation[2] is not None and self.box_centroid is not None and self.box_ratio is not None:
                if self.selfie is None and self.drone_rotation[2] is not None:
                    '''[centroid, ratio, yaw]'''
                    self.controller.init_position(self.drone_rotation[2], self.box_centroid, self.box_ratio)

                elif self.selfie is not None:
                    self.drone_status = 'selfie'
                    '''[Drone_Yaw, bbx_centroid.x, bbx_centroid.y, bbx_ratio]'''
                    self.stick = [self.drone_rotation[2], self.box_centroid[0], self.box_centroid[1], self.box_ratio]

                    '''Uncomment for control'''
                    # self.controller.selfie_position(self.selfie, self.stick)

            #self.image_pub.publish(self.bridge.cv2_to_imgmsg(detected_image, "bgr8"))

            if self.selfie:
                self.SDS.header.frame_id = 'sds'
                self.SDS.drone_state = self.drone_status
                self.SDS.face_box_centroid_x = self.selfie[1]
                self.SDS.face_box_centroid_y = self.selfie[2]
                self.SDS.face_box_ratio = self.selfie[3]

                self.SDS.fused_z_orientation = self.selfie[0]

                self.SDS.drone_yaw = self.drone_rotation[2]
                self.SDS.human_box_centroid_x = self.box_centroid[0]
                self.SDS.human_box_centroid_y = self.box_centroid[1]
                self.SDS.human_box_ratio = self.box_ratio
                self.sds_state.publish(self.SDS)

    except CvBridgeError as e:
      print(e)

