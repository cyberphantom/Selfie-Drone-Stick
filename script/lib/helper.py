#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import rospy
from itertools import *
import cv2, time, math, random, csv, os, itertools


folder = '/home/saif/catkin_ws/src/selfiestickdrone/scripts/states_actions/'
def gen_actions():
    actions = []
    final_actions=[]
    for xr in xrange(0, 105, 5):
        for yr in xrange(0,105, 5):
            for zr in xrange(0,105, 5):
                for wr in xrange(0,105, 5):
                    x = truncate(xr * 0.01)
                    y = truncate(yr * 0.01)
                    z = truncate(zr * 0.01)
                    w = truncate(wr * 0.01)
                    state = [x, y, z, w]
                    for i in list(itertools.permutations(state, 4)):
                        actions.append(i)

    actions.sort()
    sorted_non_dup = list(actions for actions, _ in itertools.groupby(actions))
    for d in xrange(2,5):
        for j in sorted_non_dup:
            l = list(j)
            l.append(d)
            ll= tuple(l)
            final_actions.append(ll)


    with open(os.path.join(folder, 'actions' + '.csv'), 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(final_actions)
    fout.close()


def gen_states():
    state = ['A', 'B', 'C', 'D']
    print(len(list(itertools.permutations(state, 4))))



def truncate(f):
    return math.floor(f * 10 ** 2) / 10 ** 2



def bounding_box(w, h, box):
    minx = int(box[0] * w)
    miny = int(box[1] * h)
    maxx = int(box[2] * w)
    maxy = int(box[3] * h)
    deltaW = maxx - minx
    deltaH = maxy - miny
    box_area = deltaW * deltaH
    box_ratio = float(box_area) / float(w * h)
    centroid = [int(deltaW / 2) + minx, int(deltaH / 2) + miny]
    return box_ratio, centroid

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



def quaternion_to_euler_angle(x, y, z, w):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z




'''
   Phone 
   Y and Z ratio 
   Y:0 (straight) Y:70 (Highest possible rotation)
   Z:-60 (left) Z:60 (right) max possible view side
   
   Drone 
   roll and altitude ratio
   alt:? (straight) alt:? (highest with view depth)
   roll:? (left) roll:? (right) how Z approperate with roll
'''

#gen_states()
#gen_actions()