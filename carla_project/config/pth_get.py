import os
import time
import pickle
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import torch
import yaml
from mmengine import Config
import numpy as np
import matplotlib.pyplot as plt
import json
import mmcv
import numpy as np
from mmengine import load
from numba.core.typing.builtins import Print

from mmdet3d.visualization import Det3DLocalVisualizer
from mmdet3d.structures import CameraInstance3DBoxes, LiDARInstance3DBoxes
import mmcv
import numpy as np
from mmengine import load

from mmdet3d.visualization import Det3DLocalVisualizer
from mmdet3d.structures import CameraInstance3DBoxes
import torch

def bevfusion_pth_to_right():
    # 加载权重文件
    path = '../../checkpoints/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-5239b1af.pth'
    model = torch.load(path)

    def transpose_weights(model, layer_names):
        for layer in layer_names:
            if layer in model['state_dict']:
                weight = model['state_dict'][layer]
                # 将权重从 [N, C, D, H, W] 转置为 [C, D, H, W, N]
                weight = weight.permute(1, 2, 3, 4, 0)  # 转置维度
                model['state_dict'][layer] = weight

    # 定义需要转置的层
    layer_names = [
        'pts_middle_encoder.conv_input.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer1.0.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer1.0.conv2.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer1.1.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer1.1.conv2.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer1.2.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.0.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.0.conv2.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.1.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.1.conv2.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.2.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.0.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.0.conv2.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.1.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.1.conv2.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.2.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer4.0.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer4.0.conv2.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer4.1.conv1.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer4.1.conv2.weight',
        'pts_middle_encoder.conv_out.0.weight'
    ]

    # 转置权重
    transpose_weights(model, layer_names)

    # 保存修改后的模型
    torch.save(model, '../../checkpoints/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-fixed.pth')


def mvxnet_pth_to_right():
    # 加载权重文件
    path = '../../checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-8963258a.pth'
    model = torch.load(path)

    def transpose_weights(model, layer_names):
        for layer in layer_names:
            if layer in model['state_dict']:
                weight = model['state_dict'][layer]
                # 将权重从 [N, C, D, H, W] 转置为 [C, D, H, W, N]
                weight = weight.permute(1, 2, 3, 4, 0)  # 交换最后一个维度和第一个维度
                model['state_dict'][layer] = weight

    # 定义需要转置的层
    layer_names = [
        'pts_middle_encoder.conv_input.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer1.0.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.0.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.1.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer2.2.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.0.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.1.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer3.2.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer4.0.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer4.1.0.weight',
        'pts_middle_encoder.encoder_layers.encoder_layer4.2.0.weight',
        'pts_middle_encoder.conv_out.0.weight'
    ]

    # 转置权重
    transpose_weights(model, layer_names)

    # 保存修改后的模型
    torch.save(model, '../../checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth')
# 读取点云数据的函数

if __name__ == "__main__":
    pass
























