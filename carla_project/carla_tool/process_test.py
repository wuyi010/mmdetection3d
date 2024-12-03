import open3d as o3d
import numpy as np
import numpy as np
from tifffile.tifffile import read_mm_header

from carla_project.carla_tool import visualize_point_cloud

import numpy as np


def read_point_cloud_ply(file_path):
    # 读取点云文件
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # 跳过头部信息
    header_end = False
    points = []
    intensities = []
    points_intensities_numpy = []

    for line in lines:
        if header_end:
            parts = line.strip().split()  # 去掉空白字符并分割
            if len(parts) == 4:  # 确保每行有4个元素 (x, y, z, intensity)
                try:
                    x, y, z, intensity = map(float, parts)
                    # 检查是否是坐标 (0, 0, 0)
                    if (x, y, z) != (0.0, 0.0, 0.0):  # 如果不是 (0, 0, 0)，则添加
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

    # 返回有效点、强度和带有强度信息的点
    return points, intensities, points_intensities_numpy



import numpy as np
import struct


def visualize_point_nuscenes(bin_path):
    import numpy as np
    import open3d as o3d



    # 将数据加载为 numpy 数组
    # 一般的 .bin 点云数据格式是 [x, y, z, intensity]，每个点占用4个float32数值

    point_cloud = np.fromfile(bin_path, dtype=np.float32).reshape(-1,3)

    print(f"点云共有 {point_cloud.shape[0]} 个点")
    print("前5个点的数据为：")
    print(point_cloud[:20])  # 打印前5个点
    min_values = point_cloud.min(axis=0)
    max_values = point_cloud.max(axis=0)
    # 打印结果
    for i in range(point_cloud.shape[1]):
        print(f"Column {i}: Min = {min_values[i]:.3f}, Max = {max_values[i]:.3f}")



    #
    # # 提取出点的坐标 [x, y, z]
    # points = point_cloud[:, :3]
    # # 创建一个 open3d 点云对象
    # pcd = o3d.geometry.PointCloud()
    # # 将 numpy 数据转为 open3d 格式
    # pcd.points = o3d.utility.Vector3dVector(points)
    # # 可视化点云
    # o3d.visualization.draw_geometries([pcd])

    # 提取 x, y, z 坐标
    points = point_cloud[:, :3]

    # 提取强度值用于颜色映射
    intensity = point_cloud[:, 3]

    visualize_point_cloud(points, intensity, keep=True)

import struct
import numpy as np


#
#
# if __name__ == "__main__":
#     # points, intensities, _ = read_point_cloud_ply("/home/didi/mmdetection3d/carla_project/Carla_data/my_lidar/000000-L5.ply")
#     # print(points.shape)
#     # # print(points)
#     # visualize_point_cloud(points, intensities, keep=True)
#
#
#     # # 读取 .bin 文件
#     # bin_path = '/carla_project/carla_dataset/my_lidar/new_layout_2.pcd'
#     # visualize_point_nuscenes(bin_path )


import struct
import numpy as np

# 定义文件路径
file_path = '/carla_project/DATA_result/Carla_data_test_1119/my_lidar/000000-L1.pcd'

# 打开并读取PCD文件
with open(file_path, 'rb') as file:
    # 跳过PCD头部
    while True:
        line = file.readline().decode('utf-8').strip()
        if line == 'DATA_result binary':
            break

    # 读取二进制数据
    points = []
    intensity = []
    timestamp = []
    ring = []

    # 按照文件格式进行解析
    num_points = 384000  # PCD文件头中的POINTS
    point_format = 'fff'  # 每个点包含 x, y, z (float32)
    intensity_format = 'B'  # intensity (uint8)
    timestamp_format = 'd'  # timestamp (double)
    ring_format = 'H'  # ring (uint16)

    # 数据读取
    for _ in range(num_points):
        # 读取一个点的所有数据 (x, y, z, intensity, timestamp, ring)
        data = file.read(
            4 * 3 + 1 + 8 + 2)  # 4 * 3 bytes for (x, y, z), 1 byte for intensity, 8 bytes for timestamp, 2 bytes for ring

        # 解包数据
        x, y, z = struct.unpack('fff', data[:12])  # 前12字节是x, y, z
        intensity_val = struct.unpack('B', data[12:13])[0]  # 第13字节是intensity
        timestamp_val = struct.unpack('d', data[13:21])[0]  # 第14-21字节是timestamp
        ring_val = struct.unpack('H', data[21:23])[0]  # 第22-23字节是ring

        # 将数据添加到对应的列表中
        points.append((x, y, z))
        intensity.append(intensity_val)
        timestamp.append(timestamp_val)
        ring.append(ring_val)

    # 将数据转换为numpy数组（可选）
    points = np.array(points)
    intensity = np.array(intensity)
    timestamp = np.array(timestamp)
    ring = np.array(ring)

# 现在points, intensity, timestamp, ring分别存储了点云的x, y, z值，以及对应的其他属性
print(f'Points:\n{points[:5]}')  # 打印前五个点
print(f'Intensity:\n{intensity[:5]}')
print(f'Timestamp:\n{timestamp[:5]}')
print(f'Ring:\n{ring[:5]}')
