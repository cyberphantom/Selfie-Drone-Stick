# ROS import
import future
import rospy
import rospkg
from geometry_msgs.msg import Twist, Vector3Stamped, Pose, PoseWithCovarianceStamped

def nextObs():
    next_st = None
    n_s = []
    while next_st is None:
        next_st = rospy.wait_for_message('/obs/pos', Pose, timeout=1)
        if next_st.orientation.x == 0 and next_st.orientation.y == 0 and next_st.orientation.z == 0 and next_st.orientation.w ==0:
           n_s = []
        else:
           n_s = [next_st.orientation.x, next_st.orientation.y, next_st.orientation.z, next_st.orientation.w]
    return n_s