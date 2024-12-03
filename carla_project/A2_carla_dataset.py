import shutil
import time

import pandas as pd
from plyfile import PlyData

import os
import numpy as np


from carla_project.carla_dataset.lidar_ply_merge import lidar_ply_merge
from carla_project.carla_simu.argparser import parse_arguments
from carla_project.carla_dataset.dataset_get import ply_to_bin,rgb_copy_file,rename_and_sort_png_files,mkdir_LIDAR_L5_and_trans_to_point_L5_bin,check_dataset




# def get_numeric_filename(file_name):
#     """从文件名中提取数字部分，供排序使用。"""
#     return int(file_name.split('-')[0])
#
# def get_numeric_filename(file_name):
#     """从文件名中提取数字部分，供排序使用。"""
#     return int(''.join(filter(str.isdigit, file_name)))
#
# def convert_ply(input_path, output_path, pc_display=None):
#     plydata = PlyData.read(input_path)  # 读取文件
#     data = plydata.elements[0].data  # 读取数据
#     data_pd = pd.DataFrame(data)  # 转换成 DataFrame
#     data_np = np.zeros(data_pd.shape, dtype=np.float32)  # 初始化数组来存储数据
#     property_names = data[0].dtype.names  # 读取属性名称
#     for i, name in enumerate( property_names):  # 通过属性读取数据
#         data_np[:, i] = data_pd[name]
#
#     print(data_np.dtype)  # 检查数据类型，应该是 float64（在初始状态），然后是 float32（在保存时）
#     print(data_np.shape)  # 检查数组的形状，行数等于点的数量，列数等于属性的数量
#     data_np[:, 1] = -data_np[:, 1]  # 修改第二列的数值为相反数
#     # data_np[:, [0, 1]] = data_np[:, [1, 0]]# 交换第1列和第2列（注意索引是从0开始的）
#
#     # print(data_np)
#
#     # 将第 1 到第 3 列保留 3 位小数
#     data_np[:, 0:3] = np.round(data_np[:, 0:3], decimals=3)
#     data_np[:, 3] = np.round(data_np[:, 3], decimals=2)
#     data_np.astype(np.float32).tofile(output_path)
#
#     print(f"Renaming: {input_path} -> {output_path}")
#
#     if pc_display:
#         # print(point_cloud)
#         visualize_point_cloud(data_np[:, :3], data_np[:, 3], keep=True)
#
# def ply_to_bin(args, dataset_path, velodyne_file_name,pc_display=None):
#
#     # PLY 文件路径
#     ply_file_path = args.save_path + args.lidar_merge_path  # 替换为您的文件路径 =  Carla_data/lidar_merge
#     # 获取所有 .ply 文件并按数字排序
#     ply_files = [f for f in os.listdir(ply_file_path) if f.endswith('.ply')]
#     ply_files.sort(key=get_numeric_filename)  # 根据数字提取排序
#     # 遍历所有 .ply 文件
#     for index, file_name in enumerate(ply_files):
#         full_file_path = os.path.join(ply_file_path, file_name)
#         # points, intensities, points_intensities_numpy = read_pcd_ply(full_file_path)
#         new_file_name = f"{index:06d}.bin"
#         bin_file_path = os.path.join(dataset_path,  velodyne_file_name+ "/" + new_file_name)  # points 文件夹
#         convert_ply(full_file_path, bin_file_path,pc_display)

# def rgb_copy_file(args, dataset_son, dataset_name):
#
#     camera_path = args.save_path + args.camera_path  # 替换为您的文件路径
#     dataset_path = os.path.join(args.save_path, dataset_name)
#     camera_id =["C1", "C2", "C3", "C4", "C5"]
#
#     camera_name_list = [f for f in os.listdir(camera_path) if f.endswith('.png')]
#     camera_name_list.sort(key=get_numeric_filename)  # 根据数字提取排序
#     print("camera_path: ", camera_name_list)
#
#     for rgb_file in camera_name_list:
#         rgb_dir_sourse_file = os.path.join(camera_path, rgb_file)
#         # print(rgb_dir_sourse_file)
#         file_name = os.path.basename(rgb_dir_sourse_file)
#         png_id = file_name.split('-')[1].split('.')[0]
#         if png_id == camera_id[0]:
#             target_dir = os.path.join(dataset_path, dataset_son[0])
#             os.makedirs(target_dir, exist_ok=True)
#             C1_id = os.path.join(target_dir, file_name)
#             shutil.copy(rgb_dir_sourse_file, C1_id)
#             print(f"copy: {rgb_dir_sourse_file} -> {C1_id}")
#
#         if png_id == camera_id[1]:
#             target_dir = os.path.join(dataset_path, dataset_son[1])
#             os.makedirs(target_dir, exist_ok=True)
#             C2_id = os.path.join(target_dir, file_name)
#             shutil.copy(rgb_dir_sourse_file, C2_id)
#             print(f"copy: {rgb_dir_sourse_file} -> {C2_id}")
#
#         if png_id == camera_id[2]:
#             target_dir = os.path.join(dataset_path, dataset_son[2])
#             os.makedirs(target_dir, exist_ok=True)
#             C3_id = os.path.join(target_dir, file_name)
#             shutil.copy(rgb_dir_sourse_file, C3_id)
#             print(f"copy: {rgb_dir_sourse_file} -> {C3_id}")
#
#         if png_id == camera_id[3]:
#             target_dir = os.path.join(dataset_path, dataset_son[3])
#             os.makedirs(target_dir, exist_ok=True)
#             C4_id = os.path.join(target_dir, file_name)
#             shutil.copy(rgb_dir_sourse_file, C4_id)
#             print(f"copy: {rgb_dir_sourse_file} -> {C4_id}")
#
#         if png_id == camera_id[4]:
#             target_dir = os.path.join(dataset_path, dataset_son[4])
#             os.makedirs(target_dir, exist_ok=True)
#             C5_id = os.path.join(target_dir, file_name)
#             shutil.copy(rgb_dir_sourse_file, C5_id)
#             print(f"copy: {rgb_dir_sourse_file} -> {C5_id}")
#
#
# def rename_and_sort_png_files(dataset_path, dataset_son):
#     # 遍历包含 "image" 的文件夹
#     for index, file_name in enumerate([d for d in dataset_son if "image" in d]):
#         son_path = os.path.join(dataset_path, file_name)
#         print(f"正在处理文件夹: {son_path}")
#
#         # 获取当前文件夹中的所有 PNG 文件
#         png_files = [f for f in os.listdir(son_path) if f.endswith('.png')]
#         # 按照文件名中的数字部分进行排序
#         png_files.sort(key=get_numeric_filename)
#         # print("png_files: ", png_files)
#
#         # 遍历并重命名文件
#         for i, png_file in enumerate(png_files):
#             old_file_path = os.path.join(son_path, png_file)
#             new_file_name = f"{i:06d}.png"  # 生成新的文件名，例如 000000.png, 000001.png
#             new_file_path = os.path.join(son_path, new_file_name)
#
#             # 重命名文件
#             shutil.move(old_file_path, new_file_path)
#             print(f"重命名: {old_file_path} -> {new_file_path}")
#
#
#
# def get_lidar_L5_ply(source_folder= 'Carla_data/lidar',destination_folder='Carla_data/lidar_L5'):
#
#     # 源文件夹和目标文件夹路径
#     # source_folder = 'Carla_data/lidar'
#     # destination_folder = 'Carla_data/lidar_L5'
#
#     # 如果目标文件夹不存在，则创建
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)
#
#     # 遍历源文件夹中的所有文件
#     for filename in os.listdir(source_folder):
#         # 检查文件是否包含 'L5' 且扩展名为 '.ply'
#         if 'L5' in filename and filename.endswith('.ply'):
#             # 源文件的完整路径
#             src_file = os.path.join(source_folder, filename)
#             # 目标文件的完整路径
#             dst_file = os.path.join(destination_folder, filename)
#             # 复制文件到目标文件夹
#             shutil.copy(src_file, dst_file)
#             print(f"Copied: {filename}")
#
#     print("所有包含 'L5' 的 .ply 文件已成功复制到 Carla_data/lidar_L5 文件夹中！")
#
#
#
#
# def lidar_L5_ply_TO_point_L5_bin(ply_file_path="Carla_data/lidar_L5",    bin_destination_folder = 'Carla_data/dataset/point_L5'):
#     # PLY 文件路径
#     # ply_file_path = "Carla_data/lidar_L5"
#     # 获取所有 .ply 文件并按数字排序
#     ply_files = [f for f in os.listdir(ply_file_path) if f.endswith('.ply')]
#     ply_files.sort(key=get_numeric_filename)  # 根据数字提取排序
#     # 如果目标文件夹不存在，则创建
#     if not os.path.exists(bin_destination_folder):
#         os.makedirs(bin_destination_folder)
#     # 遍历所有 .ply 文件
#     for index, file_name in enumerate(ply_files):
#         full_file_path = os.path.join(ply_file_path, file_name)
#         points, intensities, points_intensities_numpy = read_point_cloud_ply(full_file_path)
#         new_file_name = f"{index:06d}.bin"
#         bin_file_path = os.path.join(bin_destination_folder +"/"+ new_file_name)  # points 文件夹
#         convert_ply(full_file_path, bin_file_path)
# def mkdir_LIDAR_L5_and_trans_to_point_L5_bin():
#     source_folder_lidar = 'Carla_data/lidar'
#     destination_folder_L5 = 'Carla_data/lidar_L5'
#     bin_destination_folder = 'Carla_data/dataset/point_L5'
#     get_lidar_L5_ply(source_folder=source_folder_lidar ,destination_folder=destination_folder_L5)
#     lidar_L5_ply_TO_point_L5_bin(ply_file_path=destination_folder_L5,    bin_destination_folder = bin_destination_folder)
#


def merge_ply(args):
    # 在仿真运行完成后，处理生成的 PLY 文件
    ply_lidar_path = args.save_path + args.lidar_path  # 替换为您的文件路径
    save_dir = args.save_path + args.lidar_merge_path  # 替换为保存文件的路径
    print("ply_lidar_path:\t", ply_lidar_path)
    print("save_dir:\t\t\t", save_dir)
    lidar_ply_merge(ply_lidar_path, save_dir)

def dataset_file_mkdir(dataset_path,dataset_list_name):
    for index, file_name in enumerate(dataset_list_name):
        son_path = os.path.join(dataset_path, file_name)
        os.makedirs(son_path, exist_ok=True)
    print("mkdir file: ", dataset_path)


# def dataset_carla_generate():
#     from carla_project.A0_config import dataset_list_name_list,camera_positions_list
#     args = parse_arguments()
#     merge_ply(args)
#
#
#     # camera_positions = ['C3', 'C4', 'C1', 'C2', 'C5']
#     # dataset_list_name = ['CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK_RIGHT', 'CAM_FRONT', "points", "calibs", "labels", "ImageSets"]
#
#     # Location_list = [2, 3, 0, 1, 4]
#     # camera_positions_list = ['C3', 'C4', 'C1', 'C2', 'C5']
#     # dataset_list_name_list = ['CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK_RIGHT', 'CAM_FRONT',
#     #                           "points",
#     #                           "calibs", "labels", "ImageSets"]
#
#     dataset_path = os.path.join(args.save_path, "dataset")
#     dataset_file_mkdir(dataset_path, dataset_list_name_list)
#     ply_to_bin(args, dataset_path, dataset_list_name_list[5])
#
#     rgb_copy_file(args, "dataset", dataset_list_name_list, camera_id=camera_positions_list)
#     rename_and_sort_png_files(dataset_path, dataset_list_name_list)
#     mkdir_LIDAR_L5_and_trans_to_point_L5_bin()


from tqdm import tqdm
import os


def dataset_carla_generate():
    from carla_project.A0_config import dataset_list_name_list, camera_positions_list
    args = parse_arguments()

    # 设置进度条
    steps = [
        "check dataset",
        "Merging PLY files",
        "Converting PLY to BIN",
        "Copying RGB files",
        "Renaming and sorting PNG files",
        "Creating LIDAR files and converting to BIN"
    ]

    # 设置进度条总步数
    total_steps = len(steps)

    # Initialize tqdm for total steps
    with tqdm(total=total_steps, desc="Processing Dataset", unit="step") as pbar:

        check_dataset()
        pbar.set_description(steps[0])
        pbar.update(1)  # Move progress bar forward by 1
        time.sleep(0.1)

        merge_ply(args)
        pbar.set_description(steps[1])
        pbar.update(1)  # Move progress bar forward by 1

        time.sleep(0.1)
        # 继续执行下一个步骤
        dataset_path = os.path.join(args.save_path, "dataset")
        dataset_file_mkdir(dataset_path, dataset_list_name_list)
        pbar.set_description(steps[2])
        pbar.update(1)
        time.sleep(0.1)
        ply_to_bin(args, dataset_path, dataset_list_name_list[5])
        pbar.set_description(steps[3])
        pbar.update(1)
        time.sleep(0.1)
        rgb_copy_file(args, "dataset", dataset_list_name_list, camera_id=camera_positions_list)
        pbar.set_description(steps[4])
        pbar.update(1)
        time.sleep(0.1)
        rename_and_sort_png_files(dataset_path, dataset_list_name_list)
        pbar.set_description(steps[5])
        pbar.update(1)
        time.sleep(0.1)
        mkdir_LIDAR_L5_and_trans_to_point_L5_bin()
        pbar.update(1)  # Move progress bar forward by 1 at the end of the process
        print("Dataset generation completed.")



if __name__ == "__main__":
    dataset_carla_generate()













