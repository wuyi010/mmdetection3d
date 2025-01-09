import os

import carla
import numpy as np
import math
import pandas as pd
from carla_project.carla_tool import visualize_point_cloud
from plyfile import PlyData
from carla_project import config
from carla_project.config import carla_config

"""-----------------------------------------new----------------------"""

def save_point_cloud_as_ply(merged_points_intensities, ply_file_path):
    """
    将合并的点云数据保存为 PLY 文件，包含位置 (x, y, z) 和强度 (I) 信息。

    :param merged_points_intensities: 合并后的点云数据，形状为 (N, 4) 的 numpy 数组
    :param ply_file_path: 保存 PLY 文件的路径
    """
    # 确保目录存在
    directory = os.path.dirname(ply_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # 创建目录

    # 获取点的数量
    num_points = merged_points_intensities.shape[0]

    # 创建 PLY 文件的头部
    header = f"""ply
format ascii 1.0
element vertex {num_points}
property float32 x
property float32 y
property float32 z
property float32 I
end_header
"""
    # 将点的坐标和强度拼接成字符串
    point_data = "\n".join(
                f"{merged_points_intensities[i, 0]} {merged_points_intensities[i, 1]} "
                f"{merged_points_intensities[i, 2]} {merged_points_intensities[i, 3]}"
                for i in range(num_points)
            )
    # 继续保存点云数据
    with open(ply_file_path, 'w') as ply_file:
        ply_file.write(header)  # 写入头部信息
        np.savetxt(ply_file, merged_points_intensities, fmt='%.6f')  # 使用 numpy 保存数据
    print(f"\t\tSaved point cloud to {ply_file_path}")
def read_point_cloud_ply(file_path):
    # 读取点云文件
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # 跳过头部信息
    header_end = False
    points = []
    intensities = []
    points_intensities_numpy =[]

    for line in lines:
        if header_end:
            parts = line.strip().split()  # 去掉空白字符并分割
            if len(parts) == 4:  # 确保每行有4个元素 (x, y, z, intensity)
                try:

                        x, y, z, intensity = map(float, parts)
                        points.append([x, y, z])  # 添加XYZ点
                        intensities.append(intensity)  # 添加强度信息
                        points_intensities_numpy.append([x, y, z, intensity])
                except ValueError:
                    print(f"Warning: 无法解析行: {line}")
        elif line.startswith('end_header'):
            header_end = True

    # 使用 NumPy 将列表转换为数组
    points = np.asarray(points)  # 转换为 NumPy 数组
    intensities = np.asarray(intensities)
    # print(f"Loaded {len(points)} points with intensity.")
    return points, intensities, points_intensities_numpy
# 生成旋转矩阵
def get_rotation_matrix(pitch, yaw, roll):
    """
    拼接点云
    生成绕X（pitch），Y（yaw），Z（roll）轴旋转的旋转矩阵。
    参数顺序为：pitch -> yaw -> roll
    """
    # 将角度转换为弧度

    pitch = math.radians(pitch)
    yaw = math.radians(yaw)
    roll = math.radians(roll)

    # 绕Y轴旋转的矩阵 (pitch)
    R_pitch = np.array([
        [math.cos(pitch), 0, -math.sin(pitch)], #bianle
        [0,               1,               0],
        [math.sin(pitch), 0, math.cos(pitch)]
    ])
    # 绕Z轴旋转的矩阵 (yaw)
    R_yaw = np.array([
        [math.cos(yaw), math.sin(yaw), 0], #bianle
        [-math.sin(yaw),  math.cos(yaw), 0],
        [0, 0, 1]
    ])

    # 绕X轴旋转的矩阵 (roll)
    R_roll = np.array([  #bianle
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll), math.cos(roll)]
    ])
    # 最终旋转矩阵
    return R_yaw @ R_pitch @ R_roll

def point_cloud_updateN4(point_cloud, intensities,  location, rotation):
    transform = carla.Transform(
                carla.Location(x=location['x'], y=location['y'], z=location['z']),
          carla.Rotation(pitch=rotation['pitch'], yaw=rotation['yaw'], roll=rotation['roll']))

    # print("形状点云",point_cloud.shape) #形状点云 (151425, 3)

    point_cloud[:, 1] *= -1  # 修正carla点云y坐标相反情况
    scaled_intensities = (1.00 - intensities)

    location = transform.location
    rotation = transform.rotation
    rotation_matrix = get_rotation_matrix(rotation.pitch, rotation.yaw, rotation.roll)
    points = point_cloud @ rotation_matrix.T
    x = location.x
    y = -location.y
    z = location.z
    print([x, y, z])
    points += np.array([x, y, z])
    points[:, 2] -= 2.0  # 2.0
    point_cloud_whth_intensities = np.hstack((points, scaled_intensities.reshape(-1, 1)))
    return point_cloud_whth_intensities


