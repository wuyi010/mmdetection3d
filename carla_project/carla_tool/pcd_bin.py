import numpy as np
from pypcd import pypcd
#
# pcd_data = pypcd.PointCloud.from_path('/home/didi/mmdetection3d/carla_project/Carla_data/my_lidar/000000-L5.pcd')
# points = np.zeros([pcd_data.width, 4], dtype=np.float32)
# points[:, 0] = pcd_data.pc_data['x'].copy()
# points[:, 1] = pcd_data.pc_data['y'].copy()
# points[:, 2] = pcd_data.pc_data['z'].copy()
# points[:, 3] = pcd_data.pc_data['intensity'].copy().astype(np.float32)
# with open('/home/didi/mmdetection3d/carla_project/Carla_data/my_lidar/E1_F (Frame 0012).bin', 'wb') as f:
#     f.write(points.tobytes())
#
#
# pcd_data = pypcd.PointCloud.from_path('/home/didi/mmdetection3d/carla_project/Carla_data/my_lidar/000000-L2.pcd')
# points = np.zeros([pcd_data.width, 4], dtype=np.float32)
# points[:, 0] = pcd_data.pc_data['x'].copy()
# points[:, 1] = pcd_data.pc_data['y'].copy()
# points[:, 2] = pcd_data.pc_data['z'].copy()
# points[:, 3] = pcd_data.pc_data['intensity'].copy().astype(np.float32)
# with open('/carla_project/Carla_data/my_lidar/left_back.bin', 'wb') as f:
#     f.write(points.tobytes())
#
#
# pcd_data = pypcd.PointCloud.from_path('/home/didi/mmdetection3d/carla_project/carla_dataset/my_lidar/000000-L1.pcd')
# points = np.zeros([pcd_data.width, 4], dtype=np.float32)
# points[:, 0] = pcd_data.pc_data['x'].copy()
# points[:, 1] = pcd_data.pc_data['y'].copy()
# points[:, 2] = pcd_data.pc_data['z'].copy()
# points[:, 3] = pcd_data.pc_data['intensity'].copy().astype(np.float32)
# with open('/home/didi/mmdetection3d/carla_project/carla_dataset/my_lidar/000000-L1.ply', 'wb') as f:
#     f.write(points.tobytes())

import os
import numpy as np
import pypcd


def convert_pcd_to_ply(pcd_file, ply_file):
    # 从 PCD 文件读取点云数据
    pcd_data = pypcd.PointCloud.from_path(pcd_file)

    # 创建一个空的 NumPy 数组，准备存储点云数据
    points = np.zeros([pcd_data.width, 4], dtype=np.float32)

    # 填充点云数据 (x, y, z, intensity)
    points[:, 0] = pcd_data.pc_data['x'].copy()
    points[:, 1] = pcd_data.pc_data['y'].copy()
    points[:, 2] = pcd_data.pc_data['z'].copy()
    points[:, 3] = pcd_data.pc_data['intensity'].copy().astype(np.float32)

    # 将处理后的点云数据写入 .ply 文件
    with open(ply_file, 'wb') as f:
        f.write(points.tobytes())
    print(f"转换完成: {pcd_file} -> {ply_file}")


def process_pcd_files_in_directory(directory):
    # 获取文件夹中的所有文件
    for filename in os.listdir(directory):
        # 只处理 .pcd 文件
        if filename.endswith('.pcd'):
            pcd_file = os.path.join(directory, filename)
            ply_file = os.path.join(directory, filename.replace('.pcd', '.ply'))
            # 调用转换函数
            convert_pcd_to_ply(pcd_file, ply_file)

if __name__ == "__main__":
    # 设置文件夹路径
    pcd_directory = '/home/didi/mmdetection3d/carla_project/carla_dataset/my_lidar'

    # 调用函数处理文件夹中的所有 .pcd 文件
    process_pcd_files_in_directory(pcd_directory)
