import math
import os
import re

import numpy as np

from carla_project.carla_tool.read_point_cloud_ply import read_point_cloud_ply
from carla_project.A0_config import lidar_positions


# 生成旋转矩阵
def get_rotation_matrix(pitch, yaw, roll):
    """
    生成绕X（pitch），Y（yaw），Z（roll）轴旋转的旋转矩阵。
    参数顺序为：pitch -> yaw -> roll
    """
    # 将角度转换为弧度

    pitch = math.radians(pitch)
    yaw = math.radians(yaw)
    roll = math.radians(roll)

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

    # 最终旋转矩阵
    return R_yaw @ R_pitch @ R_roll
def point_cloud_update(point_cloud, intensities, transform):
    location = transform.location
    rotation = transform.rotation
    rotation_matrix = get_rotation_matrix(rotation.pitch, rotation.yaw, rotation.roll)
    points = point_cloud @ rotation_matrix.T
    points += np.array([location.x, location.y, location.z])
    points[:, 2] -= 2.000
    # scaled_intensities = intensities * 0.620  # 将其缩放到0-0.620
    scaled_intensities = (1.00 - intensities)#*0.62
    point_cloud_whth_intensities = np.hstack((points, scaled_intensities.reshape(-1, 1)))

    return point_cloud_whth_intensities

# 获取指定目录下所有 PLY 文件
def get_ply_files(directory):
    # 获取所有以 .ply 结尾的文件
    ply_files = [f for f in os.listdir(directory) if f.endswith('.ply')]

    # 自定义排序规则，提取文件名中的 - 前数字和 L 后数字
    def sort_key(file_name):
        match = re.match(r'(\d+)-L(\d+)', file_name)  # 匹配类似 879583-L1, 879583-L2 的文件名
        if match:
            # 按照两个部分排序，先按 - 之前的数字，再按 L 后面的数字
            return int(match.group(1)), int(match.group(2))
        return float('inf'), float('inf')  # 没有匹配到的文件放在最后

    # 按照自定义的排序规则进行排序
    sorted_ply_files = sorted(ply_files, key=sort_key)
    return sorted_ply_files

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
    print(f"Saved point cloud to {ply_file_path}")


def lidar_ply_merge(ply_dir, save_dir):
    """
    处理 LiDAR PLY 文件，将 L1-L5 的数据合并，并保存为新的 PLY 文件。
    """
    point_cloud_whth_intensities_list = []
    merged_points_intensities = []

    # 获取所有的 PLY 文件
    ply_files_order = get_ply_files(ply_dir)  # 获取所有 PLY 文件 ['346799-L1.ply', '346799-L2.ply', '346799-L3.ply',]
    print("ply_files:", ply_files_order)

    # 提取不同 LiDAR 文件的主文件名 ['346799', '346819', '346839',]
    pc_files_name = []
    for ply_file in ply_files_order:
        filename = ply_file.split('-')[0]
        if filename not in pc_files_name:
            pc_files_name.append(filename)
    print(pc_files_name)

    # 遍历每一个文件名并合并对应的 LiDAR 文件
    for name in pc_files_name:
        ply_files = [f"{name}-L{i}.ply" for i in range(1, 6)]  # L1 到 L5
        lidar_paths = [os.path.join(ply_dir, ply) for ply in ply_files]
        for i, lidar_path in enumerate(lidar_paths):
            # 加载点云和强度数据
            points, intensities,_ = read_point_cloud_ply(lidar_path)
            # 使用预定义的位置更新点云数据
            point_cloud_intensity = point_cloud_update(points, intensities, lidar_positions[i])
            point_cloud_whth_intensities_list.append(point_cloud_intensity)

        # 合并所有的点云数据
        merged_points_intensities = np.vstack(point_cloud_whth_intensities_list)
        print("merged_points_intensities shape = ", merged_points_intensities.shape)

        # 保存合并后的 PLY 文件
        ply_file_path = os.path.join(save_dir, name + ".ply")
        save_point_cloud_as_ply(merged_points_intensities, ply_file_path)

        # 清空列表以处理下一组数据
        point_cloud_whth_intensities_list.clear()
        merged_points_intensities = []  # 重新初始化为空列表