import numpy as np
import open3d as o3d

from carla_project.carla_tool import visualize_point_cloud
from carla_project.carla_tool.read_bin_file_ import read_bin_file





def load_kitti_bin_visualize(bin_path):
    """
    pkg_path:
    Returns:
    """
    data= read_bin_file(bin_path)
    visualize_point_cloud(data[:,:3], data[:,3],  keep=True)

def display_point_cloud_o3d(points):
    # 创建Open3D的PointCloud对象
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3]) # 只提取前三列 (x, y, z) 作为点云的坐标
    o3d.visualization.draw_geometries([pcd], window_name="Point Cloud Visualization")



def main():
    # # 替换为您的.bin文件路径
    # load_kitti_bin_visualize("/home/didi/mmdetection3d/data/kitti/testing/velodyne_reduced_L5/000000.bin")
    # load_kitti_bin_visualize("/home/didi/mmdetection3d/demo/data/kitti/备份_kitti/000008.bin")
    # load_kitti_bin_visualize("/carla_project/Carla_data/my_lidar/left_back.bin")


    bin_dir_carla = "/home/didi/mmdetection3d/demo/data/kitti/备份_kitti/000008.bin"
    bin_dir_carla = '/home/didi/mmdetection3d_ing/demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin'
    bin_dir_carla = '/carla_project/config/bevfusion/LidarBin/0000000036.bin'
    bin_dir_carla = '/home/didi/mmdetection3d_ing/carla_project/CarlaData/mvxnet/LidarBin/1.bin'

    load_kitti_bin_visualize(bin_dir_carla)
    points_cus = np.fromfile(bin_dir_carla, dtype=np.float32).reshape(-1,)
    print(f"点云共有 {points_cus.shape[0]} 个点")
    print("前5个点的数据为：")
    print(points_cus[:40])  # 打印前5个点
    # min_values = points_cus.min(axis=0)
    # max_values = points_cus.max(axis=0)
    # # 打印结果
    # for i in range(points_cus.shape[1]):
    #     print(f"Column {i}: Min = {min_values[i]:.3f}, Max = {max_values[i]:.3f}")





def visualize_point_nuscenes(bin_path,column):
    import numpy as np
    import open3d as o3d

    # 读取 .bin 文件


    # 将数据加载为 numpy 数组
    # 一般的 .bin 点云数据格式是 [x, y, z, intensity]，每个点占用4个float32数值
    column =column
    point_cloud = np.fromfile(bin_path, dtype=np.float32).reshape(-1, column)

    print(f"点云共有 {point_cloud.shape[0]} 个点")
    print("前5个点的数据为：")
    print(point_cloud[:50])  # 打印前5个点
    min_values = point_cloud.min(axis=0)
    max_values = point_cloud.max(axis=0)
    # 打印结果
    for i in range(point_cloud.shape[1]):
        print(f"Column {i}: Min = {min_values[i]:.3f}, Max = {max_values[i]:.3f}")



    #
    # # 提取出点的坐标 [x, y, z]
    # points = point_cloud[:, :3]
    # # 创建一个 open3d 点云对象
    # pcd = o3d.geometry.PointCloud()
    # # 将 numpy 数据转为 open3d 格式
    # pcd.points = o3d.utility.Vector3dVector(points)
    # # 可视化点云
    # o3d.visualization.draw_geometries([pcd])

    # 提取 x, y, z 坐标
    points = point_cloud[:, :3]

    # 提取强度值用于颜色映射
    intensity = point_cloud[:, 4]

    visualize_point_cloud(points,intensity, keep=True)
    #
    # # visualize_point_cloud(points, intensity, keep=True)
    #
    # # 创建 Open3D 点云对象
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(points)
    #
    # # 将强度值映射为颜色（归一化到 [0, 1]）
    # colors = np.zeros((points.shape[0], 3))  # 默认颜色为黑色
    # intensity_normalized = (intensity - intensity.min()) / (intensity.max() - intensity.min())
    # colors[:, 1] = intensity_normalized  # 用红色通道表示强度
    # pcd.colors = o3d.utility.Vector3dVector(colors)
    #
    # # 可视化点云
    # o3d.visualization.draw_geometries([pcd])


if __name__ == '__main__':
    main()



    # bin_path = '/home/didi/mmdetection3d/carla_project/Carla_data_map3_plan1_vehicle/dataset/points/000000.bin'
    # bin_path = '/home/didi/mmdetection3d/carla_project/Carla_data_map3_plan2_vehicle/dataset/points/000000.bin'
    # bin_path = '/home/didi/mmdetection3d_ing/demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin'
    bin_path = '/home/didi/mmdetection3d_ing/demo/data/nuscenes_copy/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin'
    bin_path = '/carla_project/config/bevfusion/LidarBin/0000000036.bin'

    visualize_point_nuscenes(bin_path = bin_path,column=4)

"""
点云共有 119528 个点
前5个点的数据为：
[[-61.041805   -10.523041     2.596147     0.14901961]
 [-61.071503   -10.677364     2.5984848    0.42352942]
 [-44.347282   -31.108988     2.2704122    0.14901961]
 [-44.124615   -31.109129     2.2627804    0.34901962]
 [-43.904552   -31.110075     2.2552712    0.42745098]]
Column 0: Min = -67.210, Max = 73.654
Column 1: Min = -74.628, Max = 70.556
Column 2: Min = -2.061, Max = 3.139
Column 3: Min = 0.004, Max = 0.600
点云共有 20901 个点
前5个点的数据为：
[[ 22.674677   -20.693924     1.2866354    0.1254902 ]
 [ 22.78271    -20.693724     1.2899767    0.1254902 ]
 [ 22.905834   -20.706636     1.2941637    0.12941177]
 [ 23.01545    -20.70678      1.2975774    0.1254902 ]
 [ 23.119032   -20.700996     1.3006487    0.12941177]]
Column 0: Min = 6.963, Max = 74.224
Column 1: Min = -35.022, Max = 44.193
Column 2: Min = -2.056, Max = 3.022
Column 3: Min = 0.004, Max = 0.620
点云共有 45247 个点
前5个点的数据为：
[[  3.415 -23.594   4.831   0.91 ]
 [  3.236 -23.546   4.821   0.91 ]
 [  3.118 -23.516   4.814   0.91 ]
 [  3.059 -23.5     4.811   0.91 ]
 [  2.999 -23.485   4.808   0.91 ]]
Column 0: Min = -94.714, Max = 101.654
Column 1: Min = -52.480, Max = 50.546
Column 2: Min = -2.630, Max = 19.343
Column 3: Min = 0.670, Max = 0.990

"""

