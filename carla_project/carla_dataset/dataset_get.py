import shutil

import pandas as pd
from plyfile import PlyData

import os
import numpy as np

from carla_project.carla_tool.read_point_cloud_ply import read_point_cloud_ply
from carla_project.carla_tool.visualize_point_cloud import visualize_point_cloud
from carla_project.carla_dataset.check_datadet import check_and_clean_images_and_lidar


def get_numeric_filename(file_name):
    """从文件名中提取数字部分，供排序使用。"""
    return int(file_name.split('-')[0])

def get_numeric_filename(file_name):
    """从文件名中提取数字部分，供排序使用。"""
    return int(''.join(filter(str.isdigit, file_name)))

def convert_ply(input_path, output_path, pc_display=None):
    plydata = PlyData.read(input_path)  # 读取文件
    data = plydata.elements[0].data  # 读取数据
    data_pd = pd.DataFrame(data)  # 转换成 DataFrame
    data_np = np.zeros(data_pd.shape, dtype=np.float32)  # 初始化数组来存储数据
    property_names = data[0].dtype.names  # 读取属性名称
    for i, name in enumerate( property_names):  # 通过属性读取数据
        data_np[:, i] = data_pd[name]

    print(data_np.dtype)  # 检查数据类型，应该是 float64（在初始状态），然后是 float32（在保存时）
    print(data_np.shape)  # 检查数组的形状，行数等于点的数量，列数等于属性的数量
    data_np[:, 1] = -data_np[:, 1]  # 修改第二列的数值为相反数
    # data_np[:, [0, 1]] = data_np[:, [1, 0]]# 交换第1列和第2列（注意索引是从0开始的）

    # print(data_np)

    # 将第 1 到第 3 列保留 3 位小数
    data_np[:, 0:3] = np.round(data_np[:, 0:3], decimals=3)
    data_np[:, 3] = np.round(data_np[:, 3], decimals=2)
    data_np.astype(np.float32).tofile(output_path)

    print(f"Renaming: {input_path} -> {output_path}")

    if pc_display:
        # print(point_cloud)
        visualize_point_cloud(data_np[:, :3], data_np[:, 3], keep=True)

def ply_to_bin(args, dataset_path, velodyne_file_name,pc_display=None):

    # PLY 文件路径
    ply_file_path = args.save_path + args.lidar_merge_path  # 替换为您的文件路径 =  Carla_data/lidar_merge
    # 获取所有 .ply 文件并按数字排序
    ply_files = [f for f in os.listdir(ply_file_path) if f.endswith('.ply')]
    ply_files.sort(key=get_numeric_filename)  # 根据数字提取排序
    # 遍历所有 .ply 文件
    for index, file_name in enumerate(ply_files):
        full_file_path = os.path.join(ply_file_path, file_name)
        # points, intensities, points_intensities_numpy = read_pcd_ply(full_file_path)
        new_file_name = f"{index:06d}.bin"
        bin_file_path = os.path.join(dataset_path,  velodyne_file_name+ "/" + new_file_name)  # points 文件夹
        convert_ply(full_file_path, bin_file_path,pc_display)

def rgb_copy_file(args, dataset_name,  dataset_son,   camera_id =["C1", "C2", "C3", "C4", "C5"]):

    camera_path = args.save_path + args.camera_path  # 替换为您的文件路径
    dataset_path = os.path.join(args.save_path, dataset_name)
    # camera_id =["C1", "C2", "C3", "C4", "C5"]

    camera_name_list = [f for f in os.listdir(camera_path) if f.endswith('.png')]
    camera_name_list.sort(key=get_numeric_filename)  # 根据数字提取排序
    print("camera_path: ", camera_name_list)

    for rgb_file in camera_name_list:
        rgb_dir_sourse_file = os.path.join(camera_path, rgb_file)
        # print(rgb_dir_sourse_file)
        file_name = os.path.basename(rgb_dir_sourse_file)
        png_id = file_name.split('-')[1].split('.')[0]
        if png_id == camera_id[0]:
            target_dir = os.path.join(dataset_path, dataset_son[0])
            os.makedirs(target_dir, exist_ok=True)
            C1_id = os.path.join(target_dir, file_name)
            shutil.copy(rgb_dir_sourse_file, C1_id)
            print(f"copy: {rgb_dir_sourse_file} -> {C1_id}")

        if png_id == camera_id[1]:
            target_dir = os.path.join(dataset_path, dataset_son[1])
            os.makedirs(target_dir, exist_ok=True)
            C2_id = os.path.join(target_dir, file_name)
            shutil.copy(rgb_dir_sourse_file, C2_id)
            print(f"copy: {rgb_dir_sourse_file} -> {C2_id}")

        if png_id == camera_id[2]:
            target_dir = os.path.join(dataset_path, dataset_son[2])
            os.makedirs(target_dir, exist_ok=True)
            C3_id = os.path.join(target_dir, file_name)
            shutil.copy(rgb_dir_sourse_file, C3_id)
            print(f"copy: {rgb_dir_sourse_file} -> {C3_id}")

        if png_id == camera_id[3]:
            target_dir = os.path.join(dataset_path, dataset_son[3])
            os.makedirs(target_dir, exist_ok=True)
            C4_id = os.path.join(target_dir, file_name)
            shutil.copy(rgb_dir_sourse_file, C4_id)
            print(f"copy: {rgb_dir_sourse_file} -> {C4_id}")

        if png_id == camera_id[4]:
            target_dir = os.path.join(dataset_path, dataset_son[4])
            os.makedirs(target_dir, exist_ok=True)
            C5_id = os.path.join(target_dir, file_name)
            shutil.copy(rgb_dir_sourse_file, C5_id)
            print(f"copy: {rgb_dir_sourse_file} -> {C5_id}")


def rename_and_sort_png_files(dataset_path, dataset_son):
    # 遍历包含 "image" 的文件夹
    for index, file_name in enumerate([d for d in dataset_son if "CAM" in d]):
        son_path = os.path.join(dataset_path, file_name)
        print(f"正在处理文件夹: {son_path}")

        # 获取当前文件夹中的所有 PNG 文件
        png_files = [f for f in os.listdir(son_path) if f.endswith('.png')]
        # 按照文件名中的数字部分进行排序
        png_files.sort(key=get_numeric_filename)
        # print("png_files: ", png_files)

        # 遍历并重命名文件
        for i, png_file in enumerate(png_files):
            old_file_path = os.path.join(son_path, png_file)
            new_file_name = f"{i:06d}.png"  # 生成新的文件名，例如 000000.png, 000001.png
            new_file_path = os.path.join(son_path, new_file_name)

            # 重命名文件
            shutil.move(old_file_path, new_file_path)
            print(f"重命名: {old_file_path} -> {new_file_path}")



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

def check_dataset():
    camera_directory = "/home/didi/mmdetection3d/carla_project/Carla_data/camera"
    lidar_directory = "/home/didi/mmdetection3d/carla_project/Carla_data/lidar"
    check_and_clean_images_and_lidar(camera_directory, lidar_directory)
