import math
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt


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