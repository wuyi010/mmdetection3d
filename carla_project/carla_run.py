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
import shutil
import sys

import carla
import os

from carla_project.carla_simu.run_simulation_CARGO import  run_simulation_CARGO

from carla_project.carla_simu.run_simulation_Town04 import run_simulation_Town04
from carla_project.carla_simu.run_simulation_Town03 import run_simulation_Town03
from carla_simu.run_simulation_Town10HD import run_simulation_Town10
from config import carla_config

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
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 更改工作目录为当前脚本所在目录
    os.chdir(script_dir)
    script_dir_new = os.path.dirname(os.path.abspath(__file__))
    print("xxx",script_dir_new)

    # 检查文件夹是否存在，如果存在则删
    folder_path = carla_config.CarlaDataPath['dataset_path']
    print('carla data path: {}'.format(folder_path))
    # 检查文件夹是否存在
    if os.path.exists(folder_path):
        # 删除文件夹及其中的所有内容
        shutil.rmtree(folder_path)
        print(f">>> Folder '{folder_path}' has been deleted.")
    else:
        print(f">>> Folder '{folder_path}' does not exist.")

    try:
        client = carla.Client(carla_config.Server['host'], carla_config.Server['port'])
        client.set_timeout(5.0)

        if carla_config.Selection_simulation_environment ==10:
            run_simulation_Town10( client)
        if carla_config.Selection_simulation_environment ==3:
            run_simulation_Town03( client)
        elif carla_config.Selection_simulation_environment==4:
            run_simulation_Town04(client)
        elif carla_config.Selection_simulation_environment==-1:
            run_simulation_CARGO(client)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')



if __name__ == '__main__':
    main_carla()
