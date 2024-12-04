import struct
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



from PIL import Image
# python demo/multi_modality_demo.py demo/data/kitti/000008.bin demo/data/kitti/000008.png demo/data/kitti/000008.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2  --out-dir ./outputs_my

def carla_dataset_inference_vis():

    from carla_project.carla_simu.argparser import parse_arguments
    args = parse_arguments()

    from carla_project.A2_carla_dataset import dataset_carla_generate
    dataset_carla_generate()

    from carla_project.carla_tool.B_pkl_get import generate_pkl
    generate_pkl(args)

    from carla_project.A3_carla_inference import carla_inference
    carla_inference()
    from carla_project.carla_tool.B_fun_visualizer import carla_vis_nms
    carla_vis_nms("/home/didi/mmdetection3d/carla_project/Carla_data")





if __name__ == '__main__':
    carla_dataset_inference_vis()
    # transformer_1119()

