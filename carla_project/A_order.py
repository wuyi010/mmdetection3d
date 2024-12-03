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



def transformer_1119():

    # 定义文件路径
    file_path = '/carla_project/DATA_result/Carla_data_test_1119/my_lidar/new_layout_2.pcd'
    import struct

    # 定义文件路径
    file_path = 'path_to_your_file.pcd'

    # 打开PCD文件
    with open(file_path, 'rb') as file:
        # 读取并跳过头部信息，直到找到 'DATA_result binary'
        while True:
            line = file.readline().decode('utf-8').strip()
            if line == 'DATA_result binary':
                break  # 找到 DATA_result binary 后，开始读取数据

        # 读取二进制数据
        points = []
        intensity = []
        timestamp = []
        ring = []

        num_points = 384000  # PCD文件中的点数

        # 读取每个点的二进制数据
        for _ in range(num_points):
            # 每个点的数据大小：4*3 (x, y, z) + 1 (intensity) + 8 (timestamp) + 2 (ring)
            data = file.read(4 * 3 + 1 + 8 + 2)

            if len(data) < 18:
                break  # 如果读取的数据不足，跳出循环

            # 解包数据
            x, y, z = struct.unpack('fff', data[:12])  # 前12字节是x, y, z
            intensity_val = struct.unpack('B', data[12:13])[0]  # 第13字节是intensity (uint8)
            timestamp_val = struct.unpack('d', data[13:21])[0]  # 第14-21字节是timestamp (double)
            ring_val = struct.unpack('H', data[21:23])[0]  # 第22-23字节是ring (uint16)

            # 将数据添加到对应的列表中
            points.append((x, y, z))
            intensity.append(intensity_val)
            timestamp.append(timestamp_val)
            ring.append(ring_val)

        # 输出前几个数据进行检查
        print(f'Points (first 5): {points[:5]}')
        print(f'Intensity (first 5): {intensity[:5]}')
        print(f'Timestamp (first 5): {timestamp[:5]}')
        print(f'Ring (first 5): {ring[:5]}')

    # 现在points, intensity, timestamp, ring分别存储了点云的x, y, z值，以及对应的其他属性


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

