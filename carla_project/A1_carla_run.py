#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Script that render multiple sensors in the same pygame window

By default, it renders four cameras, one LiDAR and one Semantic LiDAR.
It can easily be configure for any different number of sensors. 
To do that, check lines 290-308.
"""

import glob
import os
import sys
import time

import carla

from carla_project.A0_config import get_sensor_cfg
from carla_project.A_order import carla_dataset_inference_vis
from carla_project.carla_simu.argparser import parse_arguments
from carla_project.carla_simu.run_simulation import run_simulation
from carla_project.carla_simu.run_simulation_Town04 import run_simulation_Town04
from carla_project.carla_simu.run_simulation_Town03 import run_simulation_Town03

try:
    sys.path.append(glob.glob('/home/didi/carla_project/PythonAPI/carla_project/dist/carla_project-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
try:
    import pygame
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_q
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')



def main_carla():
    args = parse_arguments()
    import os
    import shutil

    get_sensor_cfg()

    # 检查文件夹是否存在，如果存在则删除
    folder_path = args.save_path
    if os.path.exists( folder_path):
        shutil.rmtree(folder_path)
        result = f"Folder '{folder_path}' has been deleted."
    else:
        result = f"Folder '{folder_path}' does not exist."
    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(5.0)

        town = 0

        if town==3:
            run_simulation_Town03(args, client)
        elif town==4:
            run_simulation_Town04(args, client)
        else:
            run_simulation(args, client)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main_carla()

    # carla_dataset_inference_vis()
    #  python A1_carla_run.py --res 1920x1080
