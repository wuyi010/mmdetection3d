import os

from carla_project.carla_simu import parse_arguments
from carla_project.carla_tool.read_point_cloud_ply import read_point_cloud_ply
from carla_project.carla_tool.visualize_point_cloud import visualize_point_cloud_save_png


def get_numeric_filename(file_name):
    """从文件名中提取数字部分，供排序使用。"""
    return int(''.join(filter(str.isdigit, file_name)))


if __name__ == "__main__":

    args = parse_arguments()

    # PLY 文件路径
    ply_file_path = args.save_path + args.lidar_merge_path  # 替换为您的文件路径

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
