import numpy as np
import time
import torch
import open3d as o3d
from matplotlib import pyplot as plt
import mmcv
import numpy as np
from mmengine import load
from mmdet3d.structures import CameraInstance3DBoxes
from mmdet3d.visualization import Det3DLocalVisualizer
from mmdet3d.structures import LiDARInstance3DBoxes


def draw_bboxes_3d(bbox_data,file_path):
    # 加载点云数据
    points = np.fromfile(file_path, dtype=np.float32)
    points = points.reshape(-1, 4)  # 假设.bin文件包含(x, y, z, intensity)
    # points = points.reshape(-1, 5)  # 假设.bin文件包含(x, y, z, intensity)
    print(points.shape)
    # print(points[:100])  # 打印前5个点以检查数据

    # # 定义3D边界框
    # bbox_data = [
    #     [0,0,0,6,3,3,0],
    #
    #     [44.60429763793945, -5.598748683929443, -2.0505013465881348, 4.124510765075684, 1.6924574375152588, 1.465752124786377, -0.26251888275146484], [58.08891296386719, -15.851479530334473, -1.2624642848968506, 3.991213798522949, 1.646120309829712, 1.4418553113937378, -0.0326383113861084], [64.70323944091797, -2.749974489212036, -1.9421758651733398, 4.041924953460693, 1.6594781875610352, 1.46497642993927, 3.2092387676239014], [46.89818572998047, -21.26552963256836, -1.7699121236801147, 4.327033519744873, 1.672493577003479, 1.5060601234436035, -0.09052455425262451], [55.78050994873047, -7.190772533416748, -1.985102891921997, 3.844064950942993, 1.6209383010864258, 1.4611010551452637, -0.04428219795227051], [64.82272338867188, 2.770470380783081, -1.8808319568634033, 4.1872992515563965, 1.6919138431549072, 1.4633342027664185, 3.220521926879883]
    #
    # ]

    bboxes_3d = LiDARInstance3DBoxes(torch.tensor(bbox_data))  # 创建多组3D边界框

    # 使用Open3D的Visualizer显示
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='3D Bounding Box Visualization', width=1920, height=1080)

    # 将点云转换为Open3D的点云格式
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])  # 只使用前三列(X, Y, Z)
    vis.add_geometry(pcd)
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])  # 黑色背景

    # 创建边界框的线集并添加到可视化器中
    line_sets = create_bbox_line_set(bboxes_3d)
    for line_set in line_sets:
        vis.add_geometry(line_set)

    # 运行并保持窗口开启
    vis.run()

    # 销毁窗口
    vis.destroy_window()


"""点云画3D框"""
# def draw_bboxes_3d():
#     # 加载点云数据
#     points = np.fromfile('/home/didi/mmdetection3d/demo/data/kitti/000000.bin', dtype=np.float32)
#     points = points.reshape(-1, 4)
#     print(points.shape)
#     print(points[:5])  # 打印前100个点以检查数据
#
#     # 定义3D边界框
#     bboxes_3d = LiDARInstance3DBoxes(
#         torch.tensor([[0, 0, 0, 3.8, 3, 2.8, 0]]))
#
#     bboxes_3d_2 = LiDARInstance3DBoxes(
#         torch.tensor([[47.8399658203125, -5.661894798278809, -0.6395788788795471, 4.266619682312012, 1.6315230131149292,
#      1.4917305707931519, 1.3879200220108032]]))
#
#
#     # 使用Open3D的Visualizer显示
#     vis = o3d.visualization.Visualizer()
#     vis.create_window(window_name='3D Bounding Box Visualization', width=800, height=600)
#
#     # 将点云转换为Open3D的点云格式
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(points[:, :3])
#     vis.add_geometry(pcd)
#
#     # 创建边界框的线集并添加到可视化器中
#     line_set = create_bbox_line_set(bboxes_3d)
#     line_set_2 = create_bbox_line_set(bboxes_3d_2)
#     vis.add_geometry(line_set)
#     vis.add_geometry(line_set_2)
#
#     # 运行并保持窗口开启
#     vis.run()
#
#     # 销毁窗口
#     vis.destroy_window()
# def create_bbox_line_set(box3d):
#     """将3D边界框转换为Open3D的LineSet以绘制."""
#     # 获取边界框的8个顶点
#     corners = box3d.corners.cpu().numpy()[0]
#
#     # 定义边界框的12条线段，线段由顶点对组成
#     lines = [
#         [0, 1], [1, 2], [2, 3], [3, 0],  # 下底面
#         [4, 5], [5, 6], [6, 7], [7, 4],  # 上底面
#         [0, 4], [1, 5], [2, 6], [3, 7]  # 垂直边
#     ]
#
#     # 创建LineSet对象并设置点和线段
#     line_set = o3d.geometry.LineSet()
#     line_set.points = o3d.utility.Vector3dVector(corners)
#     line_set.lines = o3d.utility.Vector2iVector(lines)
#
#     # 设置边界框线条颜色
#     line_set.paint_uniform_color([1, 0, 0])  # 红色
#
#     return line_set


# 创建3D边界框的线集
def create_bbox_line_set(bboxes_3d):
    line_set = o3d.geometry.LineSet()
    corners = bboxes_3d.corners.cpu().numpy()  # 提取每个边界框的八个角点
    lines = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # 顶面
        [4, 5], [5, 6], [6, 7], [7, 4],  # 底面
        [0, 4], [1, 5], [2, 6], [3, 7],  # 连接上下面的竖线
    ]

    line_sets = []
    for corner in corners:
        # 创建线集
        bbox_line_set = o3d.geometry.LineSet()
        bbox_line_set.points = o3d.utility.Vector3dVector(corner)
        bbox_line_set.lines = o3d.utility.Vector2iVector(lines)
        bbox_line_set.paint_uniform_color([1, 0, 0])  # 红色
        line_sets.append(bbox_line_set)

    return line_sets