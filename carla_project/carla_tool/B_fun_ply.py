import os
import pickle

import numpy as np
import yaml


from carla_project.carla_tool import visualize_point_cloud
from carla_tool import read_point_cloud_ply


def save_file(content, file_name="kitti_pkg.pkl"):
    # 先将 numpy 数组转换为普通列表
    processed_content = convert_numpy_to_list(content)


    # 使用二进制模式打开文件并保存数据
    file_extension = os.path.splitext(file_name)[1].lower()
    if file_extension == '.yml' or file_extension == '.yaml':
        with open(file_name, 'w') as f:
            yaml.dump(processed_content, f, default_flow_style=False)
            print(f"数据已保存到 {file_name}")

    elif file_extension == '.pkl':
        print(f"The file '{file_name}' is a pickle file.")
        with open(file_name, 'wb') as f:
            pickle.dump(content, f)
            print("数据已保存到->", file_name)

    else:
        print(f"The file '{file_name}' has an unsupported extension.")

def convert_numpy_to_list(data):
    """
    递归地将字典或列表中的 numpy 数组转换为普通的 Python 列表。
    """
    if isinstance(data, dict):
        return {k: convert_numpy_to_list(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_to_list(item) for item in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()  # 将 numpy 数组转换为列表
    else:
        return data


def read_pcd_ply_visualize(pkg_path):
    """
    pkg_path:
    Returns:
    """
    points, intensities,_ = read_point_cloud_ply(pkg_path)

    visualize_point_cloud(points, intensities,  keep=True)

def traverse_lidar_merge_directory(directory_path):
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"Processing file: {file_path}")
            read_pcd_ply_visualize(file_path)
            # 在这里你可以对每个文件进行处理
            # 比如你可以传递给 read_pcd_ply_visualize(file_path)
            # read_pcd_ply_visualize(file_path)
if __name__ == "__main__":

    # # 指定目录
    # ply_dir = "/home/didi/mmdetection3d/carla_project/Carla_data/lidar/"
    # ply_dir = "/home/didi/mmdetection3d/carla_project/Carla_data/lidar_merge"
    # ply_dir = "/home/didi/mmdetection3d/carla_project/Carla_data/my_lidar"
    #
    # # 获取目录下的所有 .ply 文件
    # ply_files = [f for f in os.listdir(ply_dir) if f.endswith('.ply')]

    # # 循环读取每个 .ply 文件
    # for ply_file in ply_files:
    #     ply_path = os.path.join(ply_dir, ply_file)
    #     print(f"读取文件: {ply_path}")
    #     read_pcd_ply_visualize(ply_path)

    ply_dir5= "/home/didi/mmdetection3d/carla_project/Carla_data/lidar_merge/000000.ply"
    ply_dir5= "/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/bevfusion_pkl_merge/0000000383.ply"
    ply_dir5= "/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/bevfusion_pkl_merge/0000001880.ply"
    # read_pcd_ply_visualize(ply_dir5)




    # 使用函数遍历目录
    directory = '/home/didi/mmdetection3d_ing/carla_project/CarlaData/Lidar'
    directory = '/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/bevfusion_pkl_merge'
    traverse_lidar_merge_directory(directory)

