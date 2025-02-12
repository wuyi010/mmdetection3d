import pandas as pd

import pickle
from plyfile import PlyData
import os
import numpy as np
from PIL import Image
import os
from carla_project.carla_dataset.GetCalibs import cam2img_calculate, lidar2cam_calculate, lidar2img_calculate
from carla_project.carla_tool import point_cloud_updateN4, save_point_cloud_as_ply, save_to_pickle, load_from_pickle, \
    read_point_cloud_ply, visualize_point_cloud
from carla_tool.ROI_display import ROI_add_to_PLY
from config import carla_config
from config.carla_config import sensor_intensity_map



def png_to_jpg(directory_png='/home/didi/mmdetection3d_ing/demo/data/nuscenes',
               directory_jpg='/home/didi/mmdetection3d_ing/demo/data/nuscenes'):
    def create_dataset_paths_dirs(paths):
        """ 函数：创建文件夹"""
        for path in paths:
            os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建，存在则跳过
            print(f"Folder '{path}' {'created' if not os.path.exists(path) else 'already exists'}.")

    create_dataset_paths_dirs([directory_jpg])

    # 遍历目录下的所有文件
    for filename in os.listdir(directory_png):
        # 检查文件是否以.png结尾
        if filename.endswith('.png'):  # 修改为检查.png文件
            # 构建完整的文件路径
            file_path = os.path.join(directory_png, filename)

            # 尝试打开图像文件
            try:
                # 打开PNG图像
                png_image = Image.open(file_path)

                # 转换为RGB格式（如果是PNG或其他支持透明度的格式）
                jpg_image = png_image.convert('RGB')

                # 构建新的文件名（保持文件名不变，只替换扩展名）
                new_filename = filename.replace('.png', '.jpg')  # 如果原文件是png，这里进行替换
                new_file_path = os.path.join(directory_jpg, new_filename)

                # 保存为JPG格式
                jpg_image.save(new_file_path, 'JPEG')
                print(f"Converted {file_path} to {new_file_path}")

            except Exception as e:
                print(f"Failed to convert {file_path}: {e}")

def Merge_Lidar(DATASET, ply_merge_folder):
    """
    合并不同时间戳下的 lidar 点云数据，并保存为 PLY 文件。
    :param DATASET: 包含不同时间戳 lidar 数据路径的字典。
                    格式: timestamp -> lidar -> sensor_name -> {'path': ..., 'timestamp': ...}
    :param output_folder: 合并后的 PLY 文件保存目录。
    """
    if not os.path.exists(ply_merge_folder):
        os.makedirs(ply_merge_folder)

    point_cloud_whth_intensities_list = []

    for timestamp, data in DATASET.items():
        lidar_data = data.get('lidar', {})
        # 处理每个传感器的 lidar 数据
        print(f"\t\t>>> Processing: {timestamp}")
        for sensor_name, sensor_data in lidar_data.items():
            file_path = sensor_data['path']
            points, intensities, _ = read_point_cloud_ply(file_path)
            """----------点云分层显示----------"""
            if carla_config.Layered_display:
                if sensor_name in sensor_intensity_map:
                    intensities[:] = sensor_intensity_map[sensor_name]

            """----------点云分层显示----------"""
            location = carla_config.SensorLiDAR_set[sensor_name]['location']
            rotation = carla_config.SensorLiDAR_set[sensor_name]['rotation']
            point_cloud_intensity = point_cloud_updateN4(points, intensities, location, rotation)
            """----------点云分层显示---------条件筛选：找到第三列小于等于 -2 的行-"""
            # condition = point_cloud_intensity[:, 2] <= -2.0
            # point_cloud_intensity[condition, 3] -= 0.08
            point_cloud_whth_intensities_list.append(point_cloud_intensity)


        # 合并来自不同传感器的点云数据
        merged_points_intensities = np.vstack(point_cloud_whth_intensities_list)

        # 保存合并后的点云数据为 PLY 文件
        ply_file_path = os.path.join(ply_merge_folder, timestamp + ".ply")
        save_point_cloud_as_ply(merged_points_intensities, ply_file_path)

        # 清空列表，处理下一个时间戳的数据
        point_cloud_whth_intensities_list.clear()


def Ply_to_Bin_num_pts_feats4(DATASET,ply_merge_folder, bin_file_folder, display=False):
    """
    将 PLY 文件转换为 BIN 格式并保存结果。可以选择是否可视化数据。

    :param ply_file_path: 要转换的 PLY 文件路径。
    :param bin_file_path: 保存转换后 BIN 文件的路径。
    :param bin_visualize_bool: 布尔值，是否可视化点云数据。
    """
    if not os.path.exists(bin_file_folder):
        os.makedirs(bin_file_folder)

    for timestamp, _ in DATASET.items():
        ply_file_path = os.path.join(ply_merge_folder, timestamp + ".ply")
        bin_file_path = os.path.join(bin_file_folder, timestamp + ".bin")

        # 将 PLY 转换为 BIN 格式
        plydata = PlyData.read(ply_file_path)  # 读取文件
        data = plydata.elements[0].data  # 读取数据
        data_pd = pd.DataFrame(data)  # 将数据转换为 DataFrame
        # print(data_pd.head())

        data_np = np.zeros(data_pd.shape, dtype=np.float32)  # 初始化数组来存储数据
        property_names = data[0].dtype.names  # 读取属性名称
        for i, name in enumerate(property_names):  # 通过属性读取数据
            data_np[:, i] = data_pd[name]
        # 将第 1 到第 3 列保留 3 位小数
        data_np[:, 0:3] = np.round(data_np[:, 0:3], decimals=3)
        data_np[:, 3] = np.round(data_np[:, 3], decimals=2)
        data_np.astype(np.float32).tofile(bin_file_path)

        print(f"\t\tTransform: {ply_file_path} -> {bin_file_path}")

        if display:
            # print(point_cloud)
            visualize_point_cloud(data_np[:, :3], data_np[:, 3], keep=True)


def Ply_to_Bin_num_pts_feats5(DATASET,ply_merge_folder, bin_file_folder, display=False):
    """
    将 PLY 文件转换为 BIN 格式并保存结果。可以选择是否可视化数据。

    :param ply_file_path: 要转换的 PLY 文件路径。
    :param bin_file_path: 保存转换后 BIN 文件的路径。
    :param bin_visualize_bool: 布尔值，是否可视化点云数据。
    """
    if not os.path.exists(bin_file_folder):
        os.makedirs(bin_file_folder)

    for timestamp, _ in DATASET.items():
        ply_file_path = os.path.join(ply_merge_folder, timestamp + ".ply")
        bin_file_path = os.path.join(bin_file_folder, timestamp + ".bin")

        # 将 PLY 转换为 BIN 格式
        plydata = PlyData.read(ply_file_path)  # 读取文件
        data = plydata.elements[0].data  # 读取数据
        data_pd = pd.DataFrame(data)  # 将数据转换为 DataFrame
        data_pd['c'] = 25  # 在 DataFrame 中添加名为 'ones' 的列，值全为1
        # print(data_pd.head())

        data_np = np.zeros(data_pd.shape, dtype=np.float32)  # 初始化数组来存储数据
        property_names = data[0].dtype.names  # 读取属性名称
        for i, name in enumerate(property_names):  # 通过属性读取数据
            data_np[:, i] = data_pd[name]
        # 将第 1 到第 3 列保留 3 位小数
        data_np[:, 0:3] = np.round(data_np[:, 0:3], decimals=3)
        data_np[:, 3] = np.round(data_np[:, 3], decimals=2)
        data_np.astype(np.float32).tofile(bin_file_path)

        print(f"\t\tTransform: {ply_file_path} -> {bin_file_path}")

        if display:
            # print(point_cloud)
            visualize_point_cloud(data_np[:, :3], data_np[:, 3], keep=True)

def CarlaDataSetPkl(DATASET,lidar_path, camera_path,dataset):
    # 保存字典到文件
    import os
    # 获取配置路径
    camera_folder = camera_path
    lidar_folder = lidar_path
    # 初始化字典，用于存储时间戳为 key 的字典
    # 每个时间戳包含 lidar 和 camera 两个键
    # 遍历 lidar 文件夹中的所有 .ply 文件
    for filename in os.listdir(lidar_folder):
        if filename.endswith('.ply'):
            # 分割文件名，假设格式为 SensorName_timestamp.ply
            parts = filename.split('_')
            # 获取时间戳（最后一部分去掉 .ply）
            timestamp = parts[-1].split('.')[0]
            # 获取传感器名称部分
            sensor_name = '_'.join(parts[:-1])
            # 构造文件路径
            file_path = os.path.join(lidar_folder, filename)
            # 如果字典中没有当前时间戳的条目，创建空字典
            if timestamp not in DATASET:
                DATASET[timestamp] = {'lidar': {}, 'camera': {}}

            # 将 lidar 的文件路径存储到字典中，并添加 timestamp
            location = carla_config.SensorLiDAR_set[sensor_name]['location']
            rotation = carla_config.SensorLiDAR_set[sensor_name]['rotation']
            carla_config_lidar= carla_config.SensorLiDAR_set[sensor_name]['config']
            DATASET[timestamp]['lidar'][sensor_name] = {
                'path': file_path,
                'location': location,
                'rotation': rotation,
                'config': carla_config_lidar,
                'timestamp': timestamp}

    # 遍历 camera 文件夹中的所有 .png 文件
    for filename in os.listdir(camera_folder):
        if filename.endswith('.png')or filename.endswith('.jpg'):
            # 分割文件名，假设格式为 SensorName_timestamp.png
            parts = filename.split('_')
            # 获取时间戳（最后一部分去掉 .png）
            timestamp = parts[-1].split('.')[0]
            # 获取传感器名称部分
            sensor_name = '_'.join(parts[:-1])
            # 构造文件路径
            file_path = os.path.join(camera_folder, filename)

            # 只有在 timestamp_dict 中已经有该时间戳时，才添加 camera 数据
            if timestamp in DATASET:
                # 确保字典中已经初始化了 'camera' 键
                if 'camera' not in DATASET[timestamp]:
                    DATASET[timestamp]['camera'] = {}

                # 将 camera 的文件路径存储到字典中，并添加 timestamp
                camera_config = carla_config.SensorCamera_set[sensor_name]['config']
                location = carla_config.SensorCamera_set[sensor_name]['location']
                rotation = carla_config.SensorCamera_set[sensor_name]['rotation']
                DATASET[timestamp]['camera'][sensor_name] = {
                    'path': file_path,
                    'location': location,
                    'rotation': rotation,
                    'config': camera_config,
                    'timestamp': timestamp}
    save_to_pickle(DATASET, dataset)
    print(">>>传感器参数加入DATASET")
    return DATASET



def CarlaDataSetPkl_add_point(DATASET,Bin_file_path,save_mvxnet_pkl_file):
    # 获取配置路径
    Bin_folder = Bin_file_path
    # 遍历 lidar 文件夹中的所有 .ply 文件
    for filename in os.listdir(Bin_folder):
        if filename.endswith('.bin'):
            # 分割文件名，假设格式为 SensorName_timestamp.ply
            parts = filename.split('.')
            # 获取时间戳（最后一部分去掉 .ply）
            timestamp = parts[0]
            # 构造文件路径
            file_path = os.path.join(Bin_folder, filename)
            # 只有在 DATASET 中已经有该时间戳时，才添加 camera 数据
            if timestamp in DATASET:
                # 确保字典中已经初始化了 'camera' 键
                if 'point' not in DATASET[timestamp]:
                    DATASET[timestamp]['point'] = {}
                # 将 camera 的文件路径存储到字典中，并添加 timestamp
                DATASET[timestamp]['point'] = {'path': file_path, 'timestamp': timestamp}

    save_to_pickle(DATASET, save_mvxnet_pkl_file)
    print(">>>点云信息加入")
    return DATASET
def GetCalibs(DATASET,save_mvxnet_pkl_file):
    # 遍历配置中的相机和雷达项
    print(f">>>传感器配置载入：")
    for timestamp, data in DATASET.items():
        print(f"\t\tProcessing timestamp: {timestamp}")
        # 获取相机配置
        camera_data = data['camera']
        for camera_name, camera_info in camera_data.items():
            # print(f"Processing Camera: {camera_name}")
            # 获取相机配置
            camera_path = camera_info['path']
            camera_location = camera_info['location']
            camera_rotation = camera_info['rotation']
            camera_config = camera_info['config']
            width, height = camera_config['resolution']['W'], camera_config['resolution']['H']
            fov = camera_config['options']['fov']
            # 计算相机内参和雷达到相机的变换矩阵
            cam2img = cam2img_calculate(width, height, fov)
            lidar2cam = lidar2cam_calculate(camera_location, camera_rotation)
            lidar2img = lidar2img_calculate(cam2img, lidar2cam)
            DATASET[timestamp]['camera'][camera_name].update({
                'cam2img': cam2img[:3, :3].tolist(),
                'lidar2cam': lidar2cam.tolist(),
                'lidar2img': lidar2img.tolist(),
                'R0_rect': [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            })
            # print(f"相机内参 cam2img:\n{cam2img}")
            # print(f"雷达相机 lidar2cam:\n{lidar2cam}")
            # print(f"lidar2img:\n{lidar2img}")

        # 遍历配置中的相机和雷达项
        # print(f"Processing LiDAR: ",end=" ")
        lidar_data = data['lidar']
        for lidar_name, lidar_info in lidar_data.items():
            # print(f"{lidar_name}",end=" ")
            lidar_location = lidar_info['location']
            lidar_rotation = lidar_info['rotation']
            lidar2cam = lidar2cam_calculate(lidar_location, lidar_rotation)
            DATASET[timestamp]['lidar'][lidar_name].update( {'Tr_velo_to_cam': lidar2cam.tolist()})
    save_to_pickle(DATASET, save_mvxnet_pkl_file)
    print(">>>相机和雷达内参计算")
    return(DATASET)

def generate_pkg_single_file_KITTI(DATASET,calibs_path):
    # 获取文件夹路径
    print(f">>>生成每组pkl: generate_pkg_single_file_KITTI.")
    if not os.path.exists(calibs_path):
        os.makedirs(calibs_path)
    # 遍历配置中的相机和雷达项
    sample_idx=0
    metainfo = {'categories': {'car': 0, 'truck': 1, 'trailer': 2, 'bus': 3, 'construction_vehicle': 4, 'bicycle': 5,'motorcycle': 6, 'pedestrian': 7, 'traffic_cone': 8, 'barrier': 9},'dataset': 'nuscenes','version': 'v1.0-mini','info_version': '1.1'}
    for timestamp, data in DATASET.items():
        print(f"\t\t第{sample_idx}组图像",end="\n")
        process_rgb_count=0
        camera_data = data['camera']
        images={}
        for camera_name, camera_info in camera_data.items():
            CAM_NAME = camera_name
            img_path = camera_info['path']
            cam2img=   camera_info['cam2img']
            lidar2cam=   camera_info['lidar2cam']
            cam2ego =lidar2cam
            sample_data_token = 'e3d495d4ac534d54b321f50006683844'
            # 创建字典
            camera_data_direction = {
                CAM_NAME: {
                    'img_path': img_path,
                    'cam2img': cam2img,
                    'cam2ego': cam2ego,
                    'sample_data_token': sample_data_token,
                    'timestamp': timestamp,
                    'lidar2cam': lidar2cam }}
            images.update(camera_data_direction)
            process_rgb_count =process_rgb_count + 1
        data_list = [{'sample_idx': sample_idx,
                      'token': 'ca9a282c9e77460f8360f564131a8af5',
                      'timestamp': 1532402927.647951,
                      'ego2global': [[ 0,  1, 0 , 0], [-1,  0, 0,  0], [ 0,  0, 1,  0], [ 0,  0, 0,  1]],
                      'images': images,}]
        data_nuscenes ={'metainfo':metainfo,'data_list':data_list}
        # print(data_nuscenes)
        # 保存数据为 .pkl 文件
        save_pkg_file = f'{calibs_path}/{timestamp}.pkl'
        with open(save_pkg_file, 'wb') as f:
            pickle.dump(data_nuscenes, f)
        if process_rgb_count==len(carla_config.SensorCameraName):
            print(f"保存数据为{timestamp}.pkl", end="\n")  # 输出后不换行-
        else:
            print(f"{timestamp}.pkl保存失败，数据不完整", end="\t")  # 输出后不换行-
        sample_idx += 1


def create_dataset_paths_dirs(paths):
    """ 函数：创建文件夹"""
    for path in paths:
        os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建，存在则跳过
        print(f"Folder '{path}' {'created' if not os.path.exists(path) else 'already exists'}.")

def carla_data_process(check_png_dir,check_ply_dir):
    # 用于存储无法打开的文件的名称（去除后缀）
    invalid_images = []
    valid_png={}
    # 遍历目录中的所有文件 删除不能打开的png，
    for filename in os.listdir(check_png_dir):
        # 只处理 .png 文件
        if filename.endswith('.png'):
            file_path = os.path.join(check_png_dir, filename)
            try:
                # 尝试打开图像
                with Image.open(file_path) as img:
                    # 如果打开成功，继续处理下一个文件
                    img.verify()  # 验证文件是否损坏
                time = file_path.split('_')[-1].split('.')[0]
                # 如果时间戳已存在，添加文件路径到列表中；否则创建新的列表
                if time not in valid_png:
                    valid_png[time] = [file_path]  # 创建一个新的列表并添加路径
                else:
                    valid_png[time].append(file_path)  # 将路径添加到已存在的列表中

            except Exception as e:
                # 如果图像无法打开，记录文件名（去除后缀）并删除该文件
                name, _ = os.path.splitext(filename)
                invalid_images.append(name)
                os.remove(file_path)  # 删除无法打开的图像
                print(f"Deleted invalid image: {filename}")

    print(valid_png)
    # 遍历 valid_png 字典
    keys_to_remove = []
    # 找到需要删除的时间戳（如果对应列表的长度小于5）
    for time, paths in valid_png.items():
        if len(paths) < len(carla_config.SensorCameraName):
            keys_to_remove.append(time)
    # 删除不符合条件的时间戳
    for time in keys_to_remove:
        del valid_png[time]
        print(f"Deleted time {time} due to less than 5 files")


    for filename in os.listdir(check_png_dir):
        # 只处理 .png 文件
        if filename.endswith('.png'):
            file_path = os.path.join(check_png_dir, filename)
            time_to_check = file_path.split('_')[-1].split('.')[0]
            valid_files_for_time = valid_png.get(time_to_check, [])
            if file_path  not in valid_files_for_time:
                # 如果文件不在列表中，则删除文件
                os.remove(file_path)
                print(f"Deleted {file_path} as it does not belong to the specified timestamp {valid_files_for_time}.")
    for filename in os.listdir(check_ply_dir):
        # 只处理 .ply 文件
        if filename.endswith('.ply'):
            file_path = os.path.join(check_ply_dir, filename)
            # 获取文件名中的时间戳
            time_to_check = filename.split('_')[-1].split('.')[0]
            # 检查该时间戳是否在 valid_png 中
            if time_to_check not in valid_png:
                # 如果文件不在 valid_png 中，删除该文件
                os.remove(file_path)
                print(f"Deleted {file_path} as it does not belong to the specified timestamp {time_to_check}.",end="\t")
                for truekey in valid_png:
                    print(f": {truekey}",end="\t")

import os
import re




def rename_files_in_directory(directory):
    def get_numeric_part(filename):
        # 从文件名中提取数字部分
        match = re.search(r'(\d+)', filename)
        if match:
            return int(match.group(1))
        return None

    def get_numeric_part(filename):
        # 提取文件名中的数字部分
        match = re.search(r'(\d+)', filename)
        if match:
            return int(match.group(1))
        return None

    # 创建一个字典保存文件名和对应的数字部分
    file_dict = {}

    # 获取目录下所有文件
    files = os.listdir(directory)

    # 遍历文件，提取文件名中的数字并保存到字典
    for file in files:
        numeric_part = get_numeric_part(file)
        if numeric_part is not None:
            file_dict[file] = numeric_part

    # 根据字典的 value（数字部分）进行排序
    sorted_files = sorted(file_dict.items(), key=lambda x: x[1])
    print(sorted_files)

    # 按顺序重命名文件
    # 用于保存新的文件名
    new_filenames = {}

    # 初始化变量
    i = 0
    last_value = None
    # 遍历已排序的文件
    for file, value in sorted_files:
        # 如果当前value和上一个不同，则i加1
        if value != last_value:
            i += 1
            last_value = value
        # 获取文件扩展名
        extension = os.path.splitext(file)[1]
        # 构造新的文件名，如"实验_车辆模型.png", "实验_晴天场景.png"等
        prefix = '_'.join(file.split('_')[:-1])
        new_filename = f"{prefix}_{i}{extension}"
        # 旧文件的完整路径
        old_file_path = os.path.join(directory, file)
        # 新文件的完整路径
        new_file_path = os.path.join(directory, new_filename)
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f"重命名文件: {old_file_path} -> {new_file_path}")





def bevfusion_data_process():
    # 基础路径
    base_path = "/home/didi/mmdetection3d_ing/carla_project"

    dataset_path = os.path.join(base_path, carla_config.CarlaDataPath['dataset_path'])
    lidar_path = os.path.join(base_path, carla_config.CarlaDataPath['lidar_path'])
    camera_path = os.path.join(base_path, carla_config.CarlaDataPath['camera_path'])
    bevfusion_camera_folder = os.path.join(base_path, carla_config.CarlaDataPath['bevfusion_camera_folder'])
    bevfusion_pkl_merge = os.path.join(base_path, carla_config.CarlaDataPath['bevfusion_pkl_merge'])
    bevfusion_bin_folder = os.path.join(base_path, carla_config.CarlaDataPath['bevfusion_bin_folder'])
    bevfusion_pkl_folder = os.path.join(base_path, carla_config.CarlaDataPath['bevfusion_pkl_folder'])
    bevfusion_cal_folder = os.path.join(base_path, carla_config.CarlaDataPath['bevfusion_cal_folder'])
    bevfusion_out_folder = os.path.join(base_path, carla_config.CarlaDataPath['bevfusion_out_folder'])
    bevfusion_path_name = os.path.join(base_path, carla_config.CarlaDataPath['bevfusion_path_name'])



    rename_files_in_directory(camera_path)
    rename_files_in_directory(lidar_path)
    carla_data_process(camera_path, lidar_path)

    png_to_jpg(camera_path, bevfusion_camera_folder)
    # create folder
    create_dataset_paths_dirs([dataset_path, bevfusion_path_name, ])
    if load_from_pickle(bevfusion_pkl_folder):
        print("temp 已存在，退出函数")
        return  # 退出当前函数
    """<<<数据集pkl文件生成>>>"""
    DATASET = {}

    """(1)传感器配置加入DATASET"""
    DATASET1 = CarlaDataSetPkl(DATASET, lidar_path, bevfusion_camera_folder, bevfusion_pkl_folder)

    """(2)合并不同位置下的 lidar 点云数据，并保存为 PLY 文件"""
    Merge_Lidar(DATASET, bevfusion_pkl_merge)

    """(7)添加ROI"""
    ROI_add_to_PLY(bevfusion_pkl_merge)

    """(3)PLY 文件转为bin格式 num_pts_feats = 5"""
    Ply_to_Bin_num_pts_feats5(DATASET, bevfusion_pkl_merge, bevfusion_bin_folder, display=False)

    """(4) CarlaDataSetPkl 增加点云路径信息"""
    DATASET2 = CarlaDataSetPkl_add_point(DATASET, bevfusion_bin_folder, bevfusion_pkl_folder)

    """(5) 根据sensor计算camera和lidar内参外参数"""
    GetCalibs(DATASET, bevfusion_pkl_folder)

    # """<<<数据集pkl文件生成完毕>>>"""

    """(6)KITTI格式:获取每个时间戳下的pkl文件，KITTI"""
    generate_pkg_single_file_KITTI(DATASET, bevfusion_cal_folder)

    temp = load_from_pickle(bevfusion_pkl_folder)
    print(temp)



if __name__ == "__main__":
    bevfusion_data_process()






