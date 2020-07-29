#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Vector3Stamped, Pose
from sensor_msgs.msg import CompressedImage, Image
import cv2, os
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from keras import backend as K
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import Adam, SGD
from imageio import imread
import numpy as np
from matplotlib import pyplot as plt
import rospkg
import tensorflow as tf
from dunet_model import architecture
from keras_loss_function.keras_ssd_loss import SSDLoss
from keras_layers.keras_layer_AnchorBoxes import AnchorBoxes
from keras_layers.keras_layer_DecodeDetections import DecodeDetections
from keras_layers.keras_layer_DecodeDetectionsFast import DecodeDetectionsFast
from keras_layers.keras_layer_L2Normalization import L2Normalization

from ssd_encoder_decoder.ssd_output_decoder import decode_detections, decode_detections_fast

from data_generator.object_detection_2d_data_generator import DataGenerator
from data_generator.object_detection_2d_photometric_ops import ConvertTo3Channels
from data_generator.object_detection_2d_geometric_ops import Resize
from data_generator.object_detection_2d_misc_utils import apply_inverse_transforms


def bounding_box_DUNET(w, h, box):
    minx = int(box[0])
    miny = int(box[1])
    maxx = int(box[2])
    maxy = int(box[3])
    deltaW = maxx - minx
    deltaH = maxy - miny
    box_area = deltaW * deltaH
    box_ratio = float(box_area) / float(w * h)
    centroid = [int(deltaW / 2) + minx, int(deltaH / 2) + miny]
    return box_ratio, centroid


class person_detector():

    def __init__(self):
        self.reseted = None
        self.vis_obs = Pose()
        self.bridge = CvBridge()
        self.img_height = 320
        self.img_width = 320
        self.frame = None
        self.model = architecture(image_size=(self.img_height, self.img_width, 3),
                n_classes=11,
                mode='inference',
                l2_regularization=0.0005,
                scales = [0.05, 0.15, 0.3, 0.6, 0.8],
                aspect_ratios_per_layer=[[1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                                         [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                                         [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                                         [1.0, 2.0, 0.5, 3.0, 1.0/3.0]],
                two_boxes_for_ar1=True,
                steps=None,
                offsets=[0.5, 0.5, 0.5, 0.5],
                clip_boxes=True,
                variances=[0.1, 0.1, 0.2, 0.2],
                normalize_coords=True,
                subtract_mean=[123, 117, 104],
                swap_channels=[2, 1, 0],
                confidence_thresh=0.01, # check
                iou_threshold=0.45,
                top_k=200,
                nms_max_output_size=400)

        # Set the weights path
        rospack = rospkg.RosPack()
        pkg_path = rospack.get_path('reinforced_selfiestickdrone')
        weights_path = pkg_path + '/script/face_human_detection_tracking_agent/dunet/weights/dunet_epoch-50_loss-2.4019_val_loss-2.6379.h5'

        self.model.load_weights(weights_path, by_name=True)

        adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        sgd = SGD(lr=0.001, momentum=0.9, decay=0.0, nesterov=False)
        ssd_loss = SSDLoss(neg_pos_ratio=3, alpha=1.0)

        self.model.compile(optimizer=sgd, loss=ssd_loss.compute_loss)

        self.graph = tf.get_default_graph()
        self.color = list(np.random.choice(range(0, 256, 50), size=3))

        self.classes = ['background',
                   'Christmas toy', 'coffee machine', 'potted plant', 'tissue box',
                   'robot', 'soccer ball', 'turtle bot', 'uav',
                   'fire alarm', 'tennis racket', 'person']


    def run_detect(self, frame):
        self.frame= None
        box_ratio = None
        bbx = None
        box_centroid = None
        with self.graph.as_default():
            img = cv2.resize(frame, dsize=(self.img_height, self.img_width), interpolation=cv2.INTER_NEAREST)
            np_img = np.expand_dims(img, axis=0)
            y_pred = self.model.predict(np_img)
            confidence_threshold = 0.5
            y_pred_thresh = [y_pred[k][y_pred[k, :, 1] > confidence_threshold] for k in range(y_pred.shape[0])]
            np.set_printoptions(precision=2, suppress=True, linewidth=90)

            for i, box in enumerate(y_pred_thresh[0]):
                # Transform the predicted bounding boxes for the 300x300 image to the original image dimensions.
                label = '{}: {:.2f}'.format(self.classes[int(box[0])], box[1])

                if len(box) > 0:
                    if box[0] == 11.:  # 15.
                        xmin = int(box[2] * frame.shape[1] / self.img_width)
                        ymin = int(box[3] * frame.shape[0] / self.img_height)
                        xmax = int(box[4] * frame.shape[1] / self.img_width)
                        ymax = int(box[5] * frame.shape[0] / self.img_height)
                        bbx = [xmin, ymin, xmax, ymax]
                        box_ratio, box_centroid = bounding_box_DUNET(self.img_width, self.img_height, bbx)
                        if 0.001 < box_ratio < 0.8:
                            self.frame = cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), self.color[0], thickness=2)
                            self.frame = cv2.putText(self.frame, label, (xmin, ymin - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                                     self.color[0])
                            break
                        else:
                            bbx = None
                            box_ratio = None
                            box_centroid = None


        return bbx, box_ratio, box_centroid

