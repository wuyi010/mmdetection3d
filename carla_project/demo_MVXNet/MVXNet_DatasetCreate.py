import pandas as pd

import pickle
from plyfile import PlyData
import os
import numpy as np
from carla_project.carla_dataset.GetCalibs import cam2img_calculate, lidar2cam_calculate, lidar2img_calculate
from carla_project.carla_tool import point_cloud_updateN4, save_point_cloud_as_ply, save_to_pickle, load_from_pickle, \
    read_point_cloud_ply, visualize_point_cloud
from carla_tool.ROI_display import  ROI_add_to_PLY
from config import carla_config
from config.carla_config import sensor_intensity_map
from demo_bevfusion.bevfusion_DatasetCreate import carla_data_process
 # 函数：创建文件夹
def create_dataset_paths_dirs(paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建，存在则跳过
        print(f"Folder '{path}' {'created' if not os.path.exists(path) else 'already exists'}.")
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
        if filename.endswith('.png'):
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
def CarlaDataSetPkl_add_point(DATASET,Bin_file_path,save_mvxnet_pkl_file):
    # 获取配置路径
    Bin_folder = Bin_file_path

    # 初始化字典，用于存储时间戳为 key 的字典
    # 每个时间戳包含 lidar 和 camera 两个键

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
def GetCalibs(DATASET,mvxnet_pkl_file):
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
                'cam2img': cam2img.tolist(),
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
            # 获取雷达配置
            # lidar_path = lidar_info['path']
            # lidar_config = lidar_info['config']
            lidar_location = lidar_info['location']
            lidar_rotation = lidar_info['rotation']
            # lidar2cam = lidar2cam_calculate(lidar_location, lidar_rotation)
            # DATASET[timestamp]['lidar'][lidar_name].update( {'Tr_velo_to_cam': lidar2cam.tolist()})
    save_to_pickle(DATASET, mvxnet_pkl_file)
    print(">>>相机和雷达内参计算")
    return(DATASET)
def generate_pkg_single_file_KITTI(DATASET,calibs_path):
    # 获取文件夹路径
    print(f">>>生成每组pkl: generate_pkg_single_file_KITTI.")
    if not os.path.exists(calibs_path):
        os.makedirs(calibs_path)

    # 遍历配置中的相机和雷达项
    index=0
    for timestamp, data in DATASET.items():
        index += 1
        print(f"\t\t第{index}组图像",end=" ")
        process_rgb_count=0
        camera_data = data['camera']
        for camera_name, camera_info in camera_data.items():
            sample_id = f"{camera_name}_{timestamp}"
            img_path_name_ = camera_info['path']
            height = camera_info['config']['resolution']['H']
            width = camera_info['config']['resolution']['W']
            cam2img_=   camera_info['cam2img']
            lidar2cam_=   camera_info['lidar2cam']
            lidar2img_=   camera_info['lidar2img']
            R0_rect_ = camera_info.get('R0_rect',  [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            Tr_velo_to_cam_ = lidar2cam_
            # DATASET[timestamp]['camera'][camera_name].update({'sample_id': sample_id})
            lidar_path_ = DATASET[timestamp]['point']['path']

            data = {'metainfo': {'DATASET': 'KITTI'},
            'data_list': [{'sample_id': sample_id,
                           'images': {'CAM2': {'img_path': img_path_name_,
                                               'height': height,
                                               'width': width,
                                               'cam2img': cam2img_,
                                               'lidar2cam': lidar2cam_,
                                               'lidar2img': lidar2img_},
                                      'R0_rect':R0_rect_},
                           'lidar_points': {'num_pts_feats': 4,
                                            'lidar_path': lidar_path_,
                                            'Tr_velo_to_cam': Tr_velo_to_cam_,
                                            # 'Tr_imu_to_velo': [ [0.999997615814209, 0.0007553070900030434, -0.002035825978964567,-0.8086758852005005],[-0.0007854027207940817, 0.9998897910118103, -0.014822980388998985, 0.3195559084415436],[0.002024406101554632, 0.014824540354311466, 0.9998881220817566,-0.7997230887413025], [0.0, 0.0, 0.0, 1.0]]
                                            },
                           }]}
            # 保存数据为 .pkl 文件
            save_pkg_file = f'{calibs_path}/{sample_id}.pkl'
            with open(save_pkg_file, 'wb') as f:
                pickle.dump(data, f)
                # pickle.dump(data_sourse_use, f)
            process_rgb_count+=1
            processing_camera_name = '_'.join(sample_id.split('_')[:-1])
            if process_rgb_count==len(carla_config.SensorCameraName):
                print(f"{sample_id}", end="\n")  # 输出后不换行-
            else:
                print(f"{sample_id}", end="\t")  # 输出后不换行-


def main_data_mvxnet():
    # 基础路径
    base_path = "/home/didi/mmdetection3d_ing/carla_project"

    dataset_path = os.path.join(base_path, carla_config.CarlaDataPath['dataset_path'])
    lidar_path = os.path.join(base_path, carla_config.CarlaDataPath['lidar_path'])
    camera_path = os.path.join(base_path, carla_config.CarlaDataPath['camera_path'])
    mvxnet_pkl_merge = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_pkl_merge'])
    mvxnet_bin_folder = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_bin_folder'])
    mvxnet_pkl_file = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_pkl_file'])
    mvxnet_cal_folder = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_cal_folder'])
    mvxnet_out_folder = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_out_folder'])
    mvxnet_path_name = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_path_name'])
    carla_data_process(camera_path, lidar_path)
    create_dataset_paths_dirs([dataset_path, mvxnet_path_name, ])


    if load_from_pickle(mvxnet_pkl_file):
        print("temp 已存在，退出函数")
        return  # 退出当前函数
    carla_config.Layered_display= False

    """<<<数据集pkl文件生成>>>"""
    DATASET = {}

    """(1)传感器配置加入DATASET"""
    DATASET1 = CarlaDataSetPkl(DATASET, lidar_path, camera_path, mvxnet_pkl_file)

    """(2)合并不同位置下的 lidar 点云数据，并保存为 PLY 文件"""
    Merge_Lidar(DATASET, mvxnet_pkl_merge)


    ROI_add_to_PLY(mvxnet_pkl_merge)

    """(3)PLY 文件转为bin格式 num_pts_feats = 4"""
    Ply_to_Bin_num_pts_feats4(DATASET, mvxnet_pkl_merge, mvxnet_bin_folder, display=False)

    """(4) CarlaDataSetPkl 增加点云路径信息"""
    DATASET2 = CarlaDataSetPkl_add_point(DATASET, mvxnet_bin_folder, mvxnet_pkl_file)

    """(5) 根据sensor计算camera和lidar内参外参数"""
    GetCalibs(DATASET,mvxnet_pkl_file)

    # """<<<数据集pkl文件生成完毕>>>"""

    """(6)KITTI格式:获取每个时间戳下的pkl文件，KITTI"""
    generate_pkg_single_file_KITTI(DATASET, mvxnet_cal_folder)

    temp = load_from_pickle(mvxnet_pkl_file)
    print(temp)
if __name__ == "__main__":
    main_data_mvxnet()
