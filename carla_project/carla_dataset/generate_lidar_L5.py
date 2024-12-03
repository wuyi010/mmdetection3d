import numpy as np

import os
import shutil

from carla_project.carla_dataset.dataset_get import convert_ply
from carla_project.carla_tool import read_point_cloud_ply
from carla_project.carla_tool.B_fun_png_display import get_numeric_filename


def get_lidar_L5_ply(source_folder= 'Carla_data/lidar',destination_folder='Carla_data/lidar_L5'):

    # 源文件夹和目标文件夹路径
    # source_folder = 'Carla_data/lidar'
    # destination_folder = 'Carla_data/lidar_L5'

    # 如果目标文件夹不存在，则创建
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        # 检查文件是否包含 'L5' 且扩展名为 '.ply'
        if 'L5' in filename and filename.endswith('.ply'):
            # 源文件的完整路径
            src_file = os.path.join(source_folder, filename)
            # 目标文件的完整路径
            dst_file = os.path.join(destination_folder, filename)
            # 复制文件到目标文件夹
            shutil.copy(src_file, dst_file)
            print(f"Copied: {filename}")

    print("所有包含 'L5' 的 .ply 文件已成功复制到 Carla_data/lidar_L5 文件夹中！")




def lidar_L5_ply_TO_point_L5_bin(ply_file_path="Carla_data/lidar_L5",    bin_destination_folder = 'Carla_data/dataset/point_L5'):
    # PLY 文件路径
    # ply_file_path = "Carla_data/lidar_L5"
    # 获取所有 .ply 文件并按数字排序
    ply_files = [f for f in os.listdir(ply_file_path) if f.endswith('.ply')]
    ply_files.sort(key=get_numeric_filename)  # 根据数字提取排序
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(bin_destination_folder):
        os.makedirs(bin_destination_folder)
    # 遍历所有 .ply 文件
    for index, file_name in enumerate(ply_files):
        full_file_path = os.path.join(ply_file_path, file_name)
        points, intensities, points_intensities_numpy = read_point_cloud_ply(full_file_path)
        new_file_name = f"{index:06d}.bin"
        bin_file_path = os.path.join(bin_destination_folder +"/"+ new_file_name)  # points 文件夹
        convert_ply(full_file_path, bin_file_path)


def mkdir_LIDAR_L5_and_trans_to_point_L5_bin():
    source_folder_lidar = 'Carla_data/lidar'
    destination_folder_L5 = 'Carla_data/lidar_L5'
    bin_destination_folder = 'Carla_data/dataset/point_L5'
    get_lidar_L5_ply(source_folder=source_folder_lidar ,destination_folder=destination_folder_L5)
    lidar_L5_ply_TO_point_L5_bin(ply_file_path=destination_folder_L5,    bin_destination_folder = bin_destination_folder)





if __name__ == "__main__":

    mkdir_LIDAR_L5_and_trans_to_point_L5_bin()