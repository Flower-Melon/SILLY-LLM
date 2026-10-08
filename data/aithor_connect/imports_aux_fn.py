import math
import re
import shutil
import subprocess
import time
import threading
import cv2
import numpy as np
from ai2thor.controller import Controller
from scipy.spatial import distance
from typing import Tuple
from collections import deque
import random
import os
from glob import glob

def closest_node(node, nodes, no_robot, clost_node_location):
    crps = []
    distances = distance.cdist([node], nodes)[0]
    dist_indices = np.argsort(np.array(distances))
    for i in range(no_robot):
        pos_index = dist_indices[(i * 5) + clost_node_location[i]]
        crps.append (nodes[pos_index])
    return crps

def distance_pts(p1: Tuple[float, float, float], p2: Tuple[float, float, float]):
    return ((p1[0] - p2[0]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5

def goal_satisfied(goal, objects):
    properties = {
        'SLICED': ('isSliced', True), 'BROKEN': ('isBroken', True),
        'ON': ('isToggled', True), 'OFF': ('isToggled', False),
        'COOKED': ('isCooked', True), 'OPENED': ('isOpen', True),
        'CLOSED': ('isOpen', False), 'PICKED': ('isPickedUp', True),
    }
    for obj in objects:
        if goal['name'] not in obj.get('name', '') and goal['name'] != obj.get('objectType'):
            continue
        state = goal['state']
        if state == 'HOT':
            state_ok = obj.get('temperature') == 'Hot'
        elif state is None:
            state_ok = True
        else:
            field, expected = properties[state]
            state_ok = obj.get(field) == expected
        contents = obj.get('receptacleObjectIds') or []
        contains_ok = all(any(item in object_id for object_id in contents)
                          for item in goal['contains'])
        if state_ok and contains_ok:
            return True
    return False


def goal_completion_ratio(goals, objects):
    if not goals:
        return 0.0
    return sum(goal_satisfied(goal, objects) for goal in goals) / len(goals)


def generate_video():
    if shutil.which('ffmpeg') is None:
        print('ffmpeg is not installed; skipping video generation.')
        return
    frame_rate = 5
    # input_path, prefix, char_id=0, image_synthesis=['normal'], frame_rate=5
    cur_path = os.path.dirname(__file__) + "/*/"
    for imgs_folder in glob(cur_path, recursive = False):
        view = imgs_folder.split('/')[-2]
        if not os.path.isdir(imgs_folder):
            print("The input path: {} you specified does not exist.".format(imgs_folder))
        else:
            command_set = ['ffmpeg', '-y', '-framerate', str(frame_rate), '-i',
                                '{}/img_%05d.png'.format(imgs_folder), 
                                '-pix_fmt', 'yuv420p',
                                '{}/video_{}.mp4'.format(os.path.dirname(__file__), view)]
            subprocess.call(command_set)
        


