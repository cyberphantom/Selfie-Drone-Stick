#!/usr/bin/env python

import time
import numpy as np
import pandas
import rospy
import tf
import cv2, os
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Vector3Stamped, Pose, PoseWithCovarianceStamped
from sensor_msgs.msg import CompressedImage, Image
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from hector_uav_msgs.msg import Altimeter
from sensor_msgs.msg import Imu
from std_msgs.msg import Empty
from std_msgs.msg import String
import gym
from gym import utils, spaces
from gym.utils import seeding
from gym.envs.registration import register
from lib.gazebo_connection import GazeboConnection
from face_human_detection_tracking_agent.dunet.droset_person_od import person_detector
from lib.helper import *
from lib.sds_cmd import cmdVel
import math

reg = register(
    id='sds_ddpg_cont-v0',
    entry_point='env_sds_ddpg_cont:envi',
    # timestep_limit=100,
    )


class envi(gym.Env):

    def __init__(self):

        # Gazebo
        self.g_set_state = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)

        # Publishing Nodes must be initialized before the environment
        self.takeoff_pub = rospy.Publisher('/drone/takeoff', Empty, queue_size=0)
        self.vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        self.obs_pos = rospy.Publisher('/obs/pos', Pose, queue_size=5, latch=True)
        self.pos_pub = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, latch=True)

        # comment in training
        self.sds_pub = rospy.Publisher("/sds/image_raw", Image, queue_size=10)

        # Get env. parameters from th yaml file
        self.max_alt = rospy.get_param("/alt_TH/max")
        self.min_alt = rospy.get_param("/alt_TH/min")

        self.yawMin = rospy.get_param("/yaw_TH/min")
        self.yawMax = rospy.get_param("/yaw_TH/max")

        self.ratioMin = rospy.get_param("/ratio_TH/min")
        self.ratioMax = rospy.get_param("/ratio_TH/max")

        self.f_W = rospy.get_param("/input_frame_size/w")
        self.f_H = rospy.get_param("/input_frame_size/h")
        self.step_dur = rospy.get_param("/step_duration")
        self.fail_sec_detect_TH = rospy.get_param("/failed_sec_detect_TH")
        self.steps_TH = rospy.get_param("/stepsTH")
        self.nactions = rospy.get_param("/nactions")

        #self.initPose.orientation.w = rospy.get_param('/init_state/ow')
        self.initPose = Pose()

        # Desired position based on the target that specified by the phone
        self.g_yaw = None
        self.g_cx = None
        self.g_cy = None
        self.g_ratio = None

        # Carfully discritize the drone world
        self.div_yaw = ((abs(self.yawMax) + abs(self.yawMin))/ 0.39)
        self.div_w = ((self.f_W+80) / 80)
        self.div_h = ((self.f_H+60) / 60)
        self.div_ratio = (self.ratioMax + self.ratioMin)/ 0.04

        # Descretize the states (observations)
        # The no. of state is so huge so in order to simplify the situation, we discretize
        # the space to: [13, 17, 13, 9] bins
        self.yaw_bins = pandas.cut([self.yawMin, self.yawMax], bins=self.div_yaw, retbins=True)[1] # 8 bins
        self.cx_bins = pandas.cut([-40, 680], bins=self.div_w, retbins=True)[1][1:-1] # 8 bins
        self.cy_bins = pandas.cut([-30, 390], bins=self.div_h, retbins=True)[1][1:-1] # 6 bins
        self.ratio_bins = pandas.cut([self.ratioMin, self.ratioMax], bins=self.div_ratio, retbins=True)[1] # 7 bins

        # In __init__ we establish a connection to gazebo
        self.gazebo = GazeboConnection()

        self.bridge = CvBridge()
        self.dunet = person_detector()
        self.action_space = spaces.Discrete(self.nactions)
        #self._seed()
        self.rate = rospy.Rate(10) # 10Hz = 1/10 = 0.1 sec or 10 times/s
        self.drone_status = None

        # Reset observation and reward variables
        self.failure_detect_Count = 0
        self.reset_bined_obs = []
        self.stepCount = 0
        self.reward = 0
        self.drone_shot = 0
        self.drone_shot_count = 0
        self.done = False
        self.end = False
        self.bbx, self.imu, self.drone_yaw = [], None, None
        self.img, self.box_ratio, self.box_centroid = None, None, None
        self.bined_obs, self.prev_bined_obs, self.distXY, self.prev_distXY = [], [], None, None
        self.x1, self.x2, self.y1, self.y2 = None, None, None, None

    def _reset(self):
        # Reset observation and reward variables
        self.box_ratio, self.box_centroid = None, None
        self.reset_bined_obs = []
        self.failure_detect_Count = 0
        self.stepCount = 0
        self.drone_shot_count = 0
        self.reward = 0
        self.done = False
        self.end = False

        #tar_pos = [[5, 6, 4, 2], [4, 4, 4, 2], [3, 2, 4, 3]]
        tar_pos = [[5, 6, 4, 2], [3, 2, 4, 3]]
        target = random.randint(0, 1) # Don't forget to change here
        self.bined_goal = tar_pos[target]

        # Reset every step too!
        self.bbx, self.drone_yaw = [], None
        self.box_ratio, self.box_centroid = None, None
        self.bined_obs, self.prev_bined_obs, self.distXY, self.prev_dist = [], [], None, None
        self.x1, self.x2, self.y1, self.y2 = None, None, None, None


        # Corrected: Takeff only happens once
        if self.drone_status is None:
            while (self.takeoff_pub.get_num_connections() != 0):
                try:
                    self.takeoff_sequence()
                    self.drone_status = "tookoff"
                    rospy.loginfo("Taking off completed")
                    break
                except:
                    rospy.loginfo("No subscribers to Takeoff yet, so we wait and try again")
        else:
            self.reset_pos()
            self.send_up_cmd()

        while len(self.reset_bined_obs) == 0:
            try:
                self.reset_bined_obs = self.observe()
                self.reset_bined_obs = self.observe()

            except:
                rospy.loginfo("Getting observation again!")

        return self.reset_bined_obs+self.bined_goal

    def _step(self, action):

        self.stepCount += 1
        self.reward = 0.0

        # Reset every step
        self.bbx, self.imu, self.drone_yaw = [], None, None
        self.img, self.box_ratio, self.box_centroid = None, None, None
        obs_count = 0
        cmd_vel = cmdVel(action, self.drone_speed)

        self.prev_bined_obs = self.bined_obs

        self.vel_pub.publish(cmd_vel)
        self.vel_pub.publish(cmd_vel)
        time.sleep(0.2)
        self.vel_pub.publish(cmdVel(0, 1))
        self.vel_pub.publish(cmdVel(0, 1))
        time.sleep(0.1)

        #time.sleep(self.step_dur)

        self.bined_obs = []
        self.x1, self.x2, self.y1, self.y2 = None, None, None, None

        while len(self.bined_obs) == 0 and obs_count <= self.fail_sec_detect_TH:
            try:
                self.bined_obs = self.observe()
                obs_count += 1
            except:
                rospy.loginfo("Getting observation again - Step!")

        # Get the reward and see if we reach the goal

        self.reward_function()

        return self.bined_obs+self.bined_goal, self.reward, self.done, [self.drone_shot, self.end]

    def reward_function(self):
        goal_reward = 1  # points
        fail_reward = 1  # points

        if len(self.bined_obs) != 0 or len(self.prev_bined_obs) != 0:

            if len(self.bined_obs) == 0:
                print("previous", self.prev_bined_obs, "current", self.bined_obs)
                #self.bined_obs = self.prev_bined_obs
                self.reward = -1.0
                #self.done = True
                self.end = True


            if self.x1 < 5 or self.y1 < 5 or self.x2 > 635 or self.y2 > 355:
                self.reward = -1.0
                # self.done = True
                self.end = True

            else:

                # if self.stepCount <= self.steps_TH:

                    diff0 = abs(self.bined_goal[0] - self.bined_obs[0])
                    diff1 = abs(self.bined_goal[1] - self.bined_obs[1])
                    diff2 = abs(self.bined_goal[2] - self.bined_obs[2])
                    diff3 = abs(self.bined_goal[3] - self.bined_obs[3])

                    # self.reward = -(((float(diff0) / 8.0) + (float(diff1) / 8.0) + (float(diff2) / 6.0) +
                    #                (float(diff3) / 7.0)) / 4.0)

                    if diff0 > 1:
                        self.reward -= ((float(diff0) * 21.0) / 168.0) / 4.0
                    elif diff0 == 1:
                        self.reward += 0.0
                    elif diff0 == 0:
                        self.reward += 0.1

                    if diff1 > 1:
                        self.reward -= ((float(diff1) * 21.0) / 168.0) / 4.0
                    elif diff1 == 1:
                        self.reward += 0.0
                    elif diff1 == 0:
                        self.reward += 0.1

                    if diff2 > 1:
                        self.reward -= ((float(diff2) * 28.0) / 168.0) / 4.0
                    elif diff2 == 1:
                        self.reward += 0.0
                    elif diff2 == 0:
                        self.reward += 0.1

                    if diff3 > 1:
                        self.reward -= ((float(diff3) * 24.0) / 168.0) / 4.0
                    elif diff3 == 1:
                        self.reward += 0.0
                    elif diff3 == 0:
                        self.reward += 0.1


                    if diff0 == 0 and diff1 == 0 and diff2 == 0 and diff3 == 0:
                        self.reward = 1.0
                        self.drone_shot += 1
                        # self.drone_shot_count += 1
                        # if self.drone_shot_count == 2:
                        self.done = True

                    # if self.stepCount == self.steps_TH:
                    #     self.done = True

    # return observation either [] or [Drone_Yaw, bbx_centroid.x, bbx_centroid.y, bbx_ratio]
    def observe(self):
        self.imu = None

        while self.imu is None:
           try:
               self.imu = rospy.wait_for_message('/drone/imu', Imu, timeout=5)
               self.drone_yaw = self.process_imu()
           except:
               rospy.loginfo("Current drone Imu is not ready yet, retrying for getting phone IMU")
        self.img = None
        while self.img is None:
           try:
               self.img = rospy.wait_for_message('/drone/front_camera/image_raw', Image, timeout=1)
           except:
               rospy.loginfo("Current drone Image is not ready yet")

           if self.img is not None:
               frame = self.bridge.imgmsg_to_cv2(self.img, "bgr8")
               ready_image = frame.copy()
               self.bbx = self.dunet.run_detect(ready_image)
               if len(self.bbx) !=0:
                   self.box_ratio, self.box_centroid, self.x1, self.y1, self.x2, self.y2 = bounding_box_DUNET(self.f_W, self.f_H, self.bbx)

                   '''[Drone_Yaw, bbx_centroid.x, bbx_centroid.y, bbx_ratio]'''
                   obs = [self.drone_yaw, self.box_centroid[0], self.box_centroid[1], self.box_ratio]
                   self.bined_obs = [self.to_bin(obs[0], self.yaw_bins), self.to_bin(obs[1], self.cx_bins),
                                     self.to_bin(obs[2], self.cy_bins), self.to_bin(obs[3], self.ratio_bins)]
               else:
                   self.bined_obs = []


        return self.bined_obs

    def takeoff_sequence(self, seconds_taking_off=1.0):
        # Before taking off, make sure that cmd_vel is not null to avoid drifts.
        self.vel_pub.publish(cmdVel(0, 1))
        self.takeoff_pub.publish(Empty())
        time.sleep(seconds_taking_off)

    def process_imu(self):
        if self.imu is not None:
            euler = tf.transformations.euler_from_quaternion(
                [self.imu.orientation.x, self.imu.orientation.y, self.imu.orientation.z, self.imu.orientation.w]
            )
            # roll = euler[0]
            # pitch = euler[1]
            yaw = euler[2]

            return yaw

    # Arange Value based on bins: return indices
    def to_bin(self, value, bins):
        return np.digitize(x=[value], bins=bins)[0]

    # Random Number Generator, used by the learning algorithm when generating random actions
    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # Go up and wait for 1 sec
    def send_up_cmd(self):
        self.vel_pub.publish(cmdVel(5, 1)) # 5
        time.sleep(0.8)
        self.vel_pub.publish(cmdVel(0, 1))
        time.sleep(0.5)

    # Reset position
    def reset_pos(self):
        state = ModelState()
        state.model_name = "sjtu_drone"
        # Define Initial position for _reset
        # init_pos = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [-1.4, -2.9, 0.0, 0.0, 0.0, 0.0], [-1.65, 1.8, 0.0, 0.0, 0.0, 0.0]]
        init_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # p = random.randint(0, 2)
        self.initPose.position.x = init_pos[0]
        self.initPose.position.y = init_pos[1]
        self.initPose.position.z = init_pos[2]
        self.initPose.orientation.x = init_pos[3]
        self.initPose.orientation.y = init_pos[4]
        self.initPose.orientation.z = init_pos[5]
        self.initPose.orientation.w = 0.0
        state.pose = self.initPose
        ret = self.g_set_state(state)
        loc = PoseWithCovarianceStamped()
        loc.pose.pose = self.initPose
        loc.header.frame_id = "/map"
        self.pos_pub.publish(loc)
        self.pos_pub.publish(loc)
        self.pos_pub.publish(loc)