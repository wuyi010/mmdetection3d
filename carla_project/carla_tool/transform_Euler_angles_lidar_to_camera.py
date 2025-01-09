import math
import os
import pickle
import numpy as np



from carla_project.carla_simu.get_sensor_config import get_config_positions_from_json
from carla_project.carla_tool.draw_points_on_image import draw_points_on_image


def rotation_matrix(pitch, yaw, roll):
    """
    合并不同部分点云需要的旋转矩阵
    Args:
        pitch:
        yaw:
        roll:
    Returns: R_pitch @ R_yaw @ R_roll
    """
    # 绕Y轴旋转的矩阵 (pitch)
    R_pitch = np.array([
        [math.cos(pitch), 0, -math.sin(pitch)],
        [0,               1,               0],
        [math.sin(pitch), 0, math.cos(pitch)]
    ])
    # 绕Z轴旋转的矩阵 (yaw)
    R_yaw = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw),  math.cos(yaw), 0],
        [0, 0, 1]
    ])

    # 绕X轴旋转的矩阵 (roll)
    R_roll = np.array([
        [1, 0, 0],
        [0, math.cos(roll), math.sin(roll)],
        [0, -math.sin(roll), math.cos(roll)]
    ])

    R = R_pitch @ R_yaw @ R_roll
    # print("根据相机坐标系获取的旋转矩阵:\n", R)
    return R


def transform_lidar_to_camera(pitch, yaw, roll):

    """
        将欧拉角（pitch, yaw, roll）转换为旋转矩阵，适用于相机坐标系
        z 轴为前，x 轴向左，y 轴向下。
        """
    # 将欧拉角转换为弧度
    pitch = np.radians(pitch)
    yaw = np.radians(yaw)
    roll = np.radians(roll)

    # 绕Y轴旋转的矩阵 (pitch)
    R_pitch = np.array([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]
    ])
    # 绕Z轴旋转的矩阵 (yaw)
    R_yaw = np.array([
        [math.cos(yaw), math.sin(yaw), 0],
        [-math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])
    # 绕X轴旋转的矩阵 (roll)
    R_roll = np.array([
        [1, 0, 0],
        [0, math.cos(roll), math.sin(roll)],
        [0, -math.sin(roll), math.cos(roll)]
    ])
    R_cam= R_pitch @ R_yaw @ R_roll

    # print("根据相机坐标系获取的旋转矩阵:\n", R_cam)
    R_lidar_to_camera = np.array([[0, -1, 0],
                                  [0, 0, -1],
                                  [1, 0, 0]])
    R =  R_lidar_to_camera  @  R_cam #wwwwwwxxxlll
    # print("雷达坐标系到相机坐标系的旋转矩阵\n",R)
    return R


def camera_euler_angle_transform(pitch, yaw, roll):

    #Pitch (绕 x 轴旋转)
    R_pitch = np.array([
        [1, 0, 0],
        [0, math.cos(pitch), -math.sin(pitch)],
        [0, math.sin(pitch), math.cos(pitch)]
    ])
    #Yaw (绕 y 轴旋转)

    R_yaw = np.array([
        [math.cos(yaw), 0, -math.sin(yaw)],
        [0, 1, 0],
        [math.sin(yaw), 0, math.cos(yaw)]
    ])
    # Roll (绕 z 轴旋转)
    R_roll = np.array([
        [math.cos(roll), -math.sin(roll), 0],
        [math.sin(roll), math.cos(roll), 0],
        [0, 0, 1]
    ])
    RRR = R_pitch @ R_yaw @ R_roll
    return RRR


"""
正确的
    # 绕Y轴旋转的矩阵 (pitch)
    R_pitch = np.array([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]
    ])
    # 绕Z轴旋转的矩阵 (yaw)
    R_yaw = np.array([
        [math.cos(yaw), math.sin(yaw), 0],
        [-math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])
    # 绕X轴旋转的矩阵 (roll)
    R_roll = np.array([
        [1, 0, 0],
        [0, math.cos(roll), math.sin(roll)],
        [0, -math.sin(roll), math.cos(roll)]
    ])
"""