
"""在图像上绘制点云
通过使用 draw_points_on_image，我们支持在图像上绘制点云。"""
import os

import numpy as np
import time
import torch
import open3d as o3d
from matplotlib import pyplot as plt
import mmcv
import numpy as np
from mmengine import load
from mmdet3d.structures import CameraInstance3DBoxes
from mmdet3d.visualization import Det3DLocalVisualizer
from mmdet3d.structures import LiDARInstance3DBoxes

def draw_points_on_image(name,bin_file_path,img_file_path,pkl_file_path):
    # 动态构建文件路径
    namepkg = "000008"

    bin_file_path = os.path.join(bin_file_path, f'{name}.bin')
    pkl_file_path = os.path.join(pkl_file_path, f'{name}.pkl')
    img_file_path = os.path.join(img_file_path, f'{name}.png')


    # 加载点云和信息文件
    points = np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)[:, :3]
    info_file = load(pkl_file_path)  # 根据实际情况使用合适的加载函数
    lidar2img = np.array(info_file['data_list'][0]['images']['CAM2']['lidar2img'], dtype=np.float32)
    print(lidar2img)

    # 可视化
    visualizer = Det3DLocalVisualizer()
    img = mmcv.imread(img_file_path)
    img = mmcv.imconvert(img, 'bgr', 'rgb')
    visualizer.set_image(img)
    visualizer.draw_points_on_image(points, lidar2img)
    visualizer.show()