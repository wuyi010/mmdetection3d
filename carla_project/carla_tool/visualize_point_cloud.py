import os
import time
import open3d as o3d
from matplotlib import pyplot as plt
import numpy as np

from carla_project.carla_simu.argparser import parse_arguments

"""点云可视化"""
def visualize_point_cloud(points,intensities,keep=None):
    """
    Args:
        points:      点云坐标
        intensities: 强度
        keep:         保持显示
    Returns:
    """
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    normalized_intensities = (intensities - intensities.min()) / (intensities.max() - intensities.min())
    colors = plt.get_cmap("jet")(normalized_intensities)[:, :3]  # 使用“jet”颜色映射并去掉 alpha 通道
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    # o3d.visualization.draw_geometries([point_cloud])#  可视化点云

    # 创建可视化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    # 添加点云到可视化器
    vis.add_geometry(point_cloud)
    # 设置背景颜色为黑色
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])  # 黑色背景
    if keep:
        # 可视化点云
        vis.run()
        vis.destroy_window()
    else:
        # 可视化点云，并保持窗口打开 0.5 秒
        vis.poll_events()
        vis.update_renderer()
        time.sleep(0.4)  # 显示 0.5 秒
        vis.destroy_window()




def visualize_point_cloud_save_png( points, intensities,name=None,keep=None):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    normalized_intensities = (intensities - intensities.min()) / (intensities.max() - intensities.min())
    colors = plt.get_cmap("jet")(normalized_intensities)[:, :3]  # 使用“jet”颜色映射并去掉 alpha 通道
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    # o3d.visualization.draw_geometries([point_cloud])#  可视化点云

    # 创建可视化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    # 添加点云到可视化器
    vis.add_geometry(point_cloud)
    # 设置背景颜色为黑色
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])  # 黑色背景


    if keep:

        # 可视化点云
        vis.run()
        vis.destroy_window()
    else:
        # 可视化点云，并保持窗口打开 0.5 秒
        vis.poll_events()
        vis.update_renderer()

        if name:
            # 如果提供了保存路径，保存当前可视化结果为图像
            args = parse_arguments()
            save_dir_png_lidar = args.save_path +"lidar_png"
            os.makedirs(save_dir_png_lidar, exist_ok=True)
            lidar_png_dir = os.path.join(save_dir_png_lidar, name+".png")
            if lidar_png_dir:
                vis.capture_screen_image(lidar_png_dir)
                print(f"Screen capture saved to {lidar_png_dir}")

        time.sleep(0.4)  # 显示 0.5 秒
        vis.destroy_window()