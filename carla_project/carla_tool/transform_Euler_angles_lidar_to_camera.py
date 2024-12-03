import math
import os
import pickle
import numpy as np

from carla_project.A0_config import config_sensor_options_RGBCamera
from carla_project.carla_simu import parse_arguments
from carla_project.carla_simu.sensor_config import get_config_positions_from_json
from carla_project.carla_tool.draw_points_on_image import draw_points_on_image


def rotation_matrix(pitch, yaw, roll):
    """
    将欧拉角（pitch, yaw, roll）转换为旋转矩阵，适用于相机坐标系
    z 轴为前，x 轴向左，y 轴向下。
    """
    # 将欧拉角转换为弧度
    pitch = np.radians(pitch)
    yaw = np.radians(yaw)
    roll = np.radians(roll)

    # 绕 x 轴 (向左) 的旋转矩阵
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(pitch), np.sin(pitch)],
                    [0, -np.sin(pitch), np.cos(pitch)]])

    # 绕 y 轴 (向下) 的旋转矩阵
    R_y = np.array([[np.cos(yaw), 0, np.sin(yaw)],
                    [0, 1, 0],
                    [-np.sin(yaw), 0, np.cos(yaw)]])

    # 绕 z 轴 (向前) 的旋转矩阵
    R_z= np.array([[np.cos(roll), -np.sin(roll), 0],
                    [np.sin(roll), np.cos(roll), 0],
                    [0, 0, 1]])
    """--------------------------------------------------------------------"""
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

    R = R_z @ R_y @ R_x
    R = R_pitch @ R_yaw @ R_roll
    print("根据相机坐标系获取的旋转矩阵:\n", R)
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

    # 绕 x 轴 (向左) 的旋转矩阵
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(pitch), np.sin(pitch)],
                    [0, -np.sin(pitch), np.cos(pitch)]])

    # 绕 y 轴 (向下) 的旋转矩阵
    R_y = np.array([[np.cos(yaw), 0, np.sin(yaw)],
                    [0, 1, 0],
                    [-np.sin(yaw), 0, np.cos(yaw)]])

    # 绕 z 轴 (向前) 的旋转矩阵
    R_z = np.array([[np.cos(roll), -np.sin(roll), 0],
                    [np.sin(roll), np.cos(roll), 0],
                    [0, 0, 1]])
    """--------------------------------------------------------------------"""
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

    R_cam= R_z @ R_y @ R_x
    R_cam= R_pitch @ R_yaw @ R_roll

    print("根据相机坐标系获取的旋转矩阵:\n", R_cam)
    # 雷达坐标系到相机坐标系的旋转矩阵
    R_lidar_to_camera = np.array([[0, -1, 0],
                                  [0, 0, -1],
                                  [1, 0, 0]])
    # 计算相机的旋转矩阵
    # 完整变换矩阵
    R =  R_lidar_to_camera  @  R_cam #wwwwwwxxxlll
    print("雷达坐标系到相机坐标系的旋转矩阵\n",R)
    return R





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