#!/usr/bin/env python
from commands_agent.commandsAgent import command
import rospy


class controller:

    def __init__(self):

        self.errCentroid_x = 0
        self.errCentroid_y = 0
        self.errAlt = 0
        self.errCanvas_x = 0
        self.errCanvas_y = 0
        self.gaz = 0    #altitude
        self.yaw = 0    #yaw angle
        self.theta = 0
        self.phi = 0
        self.errTheta = 0
        self.errPhi = 0
        self.com = command() #saif
        self.errYaw = 0
        self.errAlt = 0



        '''Selfie'''
        self.errDepth = 0
        self.errYawCorr = 0
        self.errRollCorr = 0
        self.errAltCorr = 0
        self.eR = 0.9
        self.eY = 0.009


        '''Thresholds'''
        self.eYaw = 0.01
        self.eCX = 0.0156
        self.eCY = 0.02
        self.eR = 0.0025
        self.center_X = 320.00
        self.center_Y = 180.00
        self.yaw_max = 60



    def init_position(self, yaw, centroid, ratio):




        if centroid is not None:

            '''yaw initialization'''
            errYaw = yaw
            if abs(errYaw) > self.eYaw:
                self.yaw = pid_update(errYaw, self.errYaw, 3)  # Correct Yaw
            elif abs(errYaw) <= self.eYaw:
                self.yaw = 0
            self.errYaw = errYaw

            '''roll initialization'''
            errCentroid_x = _dst(centroid[0], self.center_X)
            if abs(errCentroid_x) > self.eCX:
                self.theta = pid_update(errCentroid_x, self.errCentroid_x, 1) #roll
            elif abs(errCentroid_x) <= self.eCX:
                self.theta = 0
            self.errCentroid_x = errCentroid_x

            errCentroid_y = _dst(centroid[1], self.center_Y)
            if abs(errCentroid_y) > self.eCY:
                self.gaz = -pid_update(errCentroid_y, self.errCentroid_y, 2) #alt
            elif abs(errCentroid_y) <= self.eCY:
                self.gaz = 0
            self.errCentroid_y = errCentroid_y

            '''Depth initialization'''
            errPhi = _dst(ratio, 0.2)
            '''Human between 0.2 and 0.03'''
            if abs(errPhi) > self.eR:
                self.phi = pid_update(errPhi, self.errPhi, 0)  # x
            elif abs(errPhi) <= self.eR:
                self.Phi = 0
            self.errPhi = errPhi

            # '''Altitude initialization'''
            # errAlt =  1.00 - imu.position.z
            # if abs(errAlt) >= 0.1:
            #     self.gaz = pid_update(errAlt, self.errAlt, 2)  # alt
            # elif abs(errAlt) < 0.1:
            #     self.gaz = 0
            # self.errAlt = errAlt

            self.com.Velocity(-self.phi, -self.theta, self.gaz, -self.yaw)

        else:
            self.com.hover()


    def selfie_position(self, selfiestate, dronestate):

        '''Velocities'''
        phi = 0
        theta = 0
        yaw = 0
        gaz = 0



        '''bounding box ratio'''
        drone_bbx_min = 0.03
        drone_bbx_max = 0.2
        selfie_bbx_ratio = selfiestate[3]
        drone_bbx_ratio_state = dronestate[3]

        stick_bbx_ratio = get_drone_y1(selfie_bbx_ratio)


        '''Yaw angle'''
        device_yaw = selfiestate[0]
        drone_yaw_state = dronestate[0]

        selfie_yaw = device_yaw


        '''Sides for rolling'''
        device_centroid_x = selfiestate[1]
        drone_centroid_x_state = dronestate[1]

        stick_centroid_x = float(5.4 * device_centroid_x)


        '''Vertical altitude'''
        drone_centroid_y_state = dronestate[2]
        device_centroid_y = selfiestate[2]

        stick_centroid_y = float(2.3 * device_centroid_y)


        if drone_centroid_x_state > 0 and drone_centroid_y_state > 0 and drone_bbx_ratio_state >= 0.03 and \
                drone_bbx_ratio_state <= 0.2:

            ''' Correct Depth '''
            if stick_bbx_ratio <= drone_bbx_max and stick_bbx_ratio >= drone_bbx_min:
                errDepth = dst(stick_bbx_ratio, drone_bbx_ratio_state, drone_bbx_max)
                if abs(errDepth) > self.eR:
                    phi = pid_update(errDepth, self.errDepth, 0)  # x
                    self.errDepth = errDepth
                elif abs(errDepth) <= self.eR:
                    phi = 0
            else:
                phi = 0


            ''' Correct roll and yaw '''
            '''
            device yaw around z axis +ve to the right -ve to the left -60 ---- 60 facing the face
            If device yaw to the left move the drone to the left and correct drone yaw to be the same as device yaw
            centering the object in the middle of the frame
    
            Drone Yaw same as phone yaw angle: wait until drone yaw got corrected by roll
            +ve to the right -ve to the left and  of the drone coordinate,
            '''

            '''roll and yaw correction
             depends on the centroids and phone yaw'''
            errRollCorr = dst(stick_centroid_x, drone_centroid_x_state, self.center_X)
            errYawCorr = dst(selfie_yaw, drone_yaw_state, self.yaw_max)

            if (abs(errRollCorr) > self.eCX or abs(errYawCorr) > self.eYaw) and (drone_centroid_x_state >= 40 and drone_centroid_x_state <= 600):
                theta = pid_update(errRollCorr, self.errRollCorr, 1) # roll
                yaw = pid_update(errYawCorr, self.errYawCorr, 3)  # Correct Yaw
                self.errYawCorr = errYawCorr
                self.errRollCorr = errRollCorr

            if abs(errRollCorr) <= self.eCX:
                theta = 0

            if abs(errYawCorr) <= self.eYaw:
                yaw = 0

            if abs(errRollCorr) <= self.eCX and abs(errYawCorr) <= self.eYaw:
                theta = 0
                yaw = 0
                #self.eCX, self.eYaw = thresholds(abs(self.eR))





            errAltCorr = dst(stick_centroid_y, drone_centroid_y_state, self.center_Y)
            if abs(errAltCorr) > self.eCY:
                gaz = pid_update(errAltCorr, self.errAltCorr, 2)  # alt

            elif abs(errAltCorr) <= self.eCY:
                gaz = 0
            self.errAltCorr = errAltCorr



            self.com.Velocity(phi, theta, gaz, yaw)
            # print('yaw:', int(selfie_yaw), int(drone_yaw_state), 'center x:', int(stick_centroid_x), int(drone_centroid_x_state), 'center y:', int(stick_centroid_y),
            #       int(drone_centroid_y_state), 'BBX ratio:',"%.3f" % stick_bbx_ratio, "%.3f" % drone_bbx_ratio_state)
            # rospy.loginfo("yaw: %.3f, %.3f" % (selfie_yaw, drone_yaw_state) + ' center_x: ' + str(stick_centroid_x)
            #               + ", " + str(drone_centroid_x_state) + ' center_y: ' + str(stick_centroid_y) + ", " +
            #               str(drone_centroid_y_state) + ' BBX ratio: %.3f, %.3f' % (stick_bbx_ratio, drone_bbx_ratio_state))
        else:
            self.com.hover()





'''[hrx, hry, alt, yaw]'''
def pid_update(error, error_data, v, kp = [0.5, 0.35, 0.35, 0.35], ki = [0.05, 0.05, 0.05, 0.05], kd = [0.05, 0.05, 0.05, 0.05]):
    return kp[v] * error + ki[v] * (error + error_data) + kd[v] * (error - error_data)

def _dst(ctr, siz):
    # if x is - the centroid to the left, else to the right
    return float(ctr - siz) / float(siz)

def dst(v2, v1, scl):
    # if x is - the centroid to the left, else to the right
    return (v2 - v1) / scl

'''Find y1'''
def get_drone_y1(x1):
    '''bbx_ratio: slop = 1.7 with this mins and maxs, phone: (x1, x2) = (0.1, 0.2), drone:
    (y1, y2) = (0.03, 0.2)'''
    #y1 = 0.2 - (0.34 - float(1.7*x1))
    y1 = 0.2 - (0.2 - float(1.7*x1))
    return y1

def thresholds(err_roll=0.9):
    if err_roll >= 0.1:
        eRoll = err_roll - 0.1
        eYaw = eRoll* 0.1

    else:
        eRoll = 0.1
        eYaw = 0.01

    return eRoll, eYaw