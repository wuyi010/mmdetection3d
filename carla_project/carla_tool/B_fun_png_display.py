import os


from carla_project import config as config


def get_numeric_filename(file_name):
    """从文件名中提取数字部分，供排序使用。"""
    return int(''.join(filter(str.isdigit, file_name)))


if __name__ == "__main__":


    # PLY 文件路径

    ply_file_path = config.CarlaDataPath['dataset_path'] + config.CarlaDataPath['lidar_merge_path']

    # 获取所有 .ply 文件并按数字排序
    ply_files = [f for f in os.listdir(ply_file_path) if f.endswith('.ply')]
    ply_files.sort(key=get_numeric_filename)  # 根据数字提取排序

    # 遍历所有 .ply 文件
    for file_name in ply_files:
        full_file_path = os.path.join(ply_file_path, file_name)

        # 读取点云和强度信息
        points, intensities ,_ = read_point_cloud_ply(full_file_path)

        # 打印点云信息
        print(f"Loaded {len(points)} points with intensity from {file_name}.")

        # 可视化点云
        visualize_point_cloud_save_png(points, intensities, file_name ,keep=True)

        # 可以选择暂停一下，等待用户按键继续
        input("Press Enter to continue to the next point cloud...")
