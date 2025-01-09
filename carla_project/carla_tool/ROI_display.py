import numpy as np
import os

from carla_tool import save_point_cloud_as_ply, read_point_cloud_ply
from config import carla_config


# 获取立方体的8个角点，中心为(0, 0, 0)
def get_cube_vertices(center, length, width, height):
    vertices = np.array([
        [length / 2, width / 2, height / 2],
        [-length / 2, width / 2, height / 2],
        [length / 2, -width / 2, height / 2],
        [-length / 2, -width / 2, height / 2],
        [length / 2, width / 2, -height / 2],
        [-length / 2, width / 2, -height / 2],
        [length / 2, -width / 2, -height / 2],
        [-length / 2, -width / 2, -height / 2],
    ])
    return vertices + center  # 返回以(0, 0, 0)为中心的角点


# 获取立方体12条边的连接关系
def get_cube_edges(vertices):
    edges = [
        [vertices[0], vertices[1]],
        [vertices[0], vertices[2]],
        [vertices[1], vertices[3]],
        [vertices[2], vertices[3]],
        [vertices[4], vertices[5]],
        [vertices[4], vertices[6]],
        [vertices[5], vertices[7]],
        [vertices[6], vertices[7]],
        [vertices[0], vertices[4]],
        [vertices[1], vertices[5]],
        [vertices[2], vertices[6]],
        [vertices[3], vertices[7]],
    ]
    return edges


# 获取立方体的6个面，每个面包含4个顶点
def get_cube_faces(vertices):
    faces = [
        # [vertices[0], vertices[1], vertices[3], vertices[2]],  # 上表面
        # [vertices[4], vertices[5], vertices[7], vertices[6]],  # 下表面
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # 前表面
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # 后表面
        [vertices[0], vertices[2], vertices[6], vertices[4]],  # 左表面
        [vertices[1], vertices[3], vertices[7], vertices[5]],  # 右表面
    ]
    return faces


# 计算两点之间的距离
def calculate_distance(point1, point2):
    return np.linalg.norm(point1 - point2)


# 在每条边上进行插值，生成多个点来连接立方体的顶点，插值点密度保持一致
def interpolate_edges(edges, total_points=300):
    # 先计算所有边的总长度
    edge_lengths = [calculate_distance(edge[0], edge[1]) for edge in edges]
    total_length = sum(edge_lengths)

    interpolated_points = []

    # 根据每条边的长度，按比例分配插值点的数量
    for edge, length in zip(edges, edge_lengths):
        num_points = max(2, int(total_points * (length / total_length)))  # 确保每条边至少有两个点
        start, end = edge
        for t in np.linspace(0, 1, num_points):
            interpolated_point = start * (1 - t) + end * t
            interpolated_points.append(interpolated_point)

    return np.array(interpolated_points)


# 在每个面上进行插值，生成更多点以覆盖整个面
def interpolate_faces(faces, total_points=600):
    interpolated_points = []

    # 为每个面进行插值
    for face in faces:
        # 选择一个三角形或四边形区域，进行插值
        # 对角线插值连接 (0, 1, 2) 和 (0, 2, 3)
        triangle1 = [face[0], face[1], face[2]]
        triangle2 = [face[0], face[2], face[3]]

        # 生成插值点
        for tri in [triangle1, triangle2]:
            for t1 in np.linspace(0, 1, int(np.sqrt(total_points / 2))):
                for t2 in np.linspace(0, 1 - t1, int(np.sqrt(total_points / 2))):
                    point = tri[0] * (1 - t1 - t2) + tri[1] * t1 + tri[2] * t2
                    interpolated_points.append(point)

    return np.array(interpolated_points)


# 主函数
def add_cube_to_point_cloud_ply(input_ply, output_ply, length, width, height, xx=0, yy=0, zz=0, roi_intensities=0,
                                total_interpolation_points=1000):
    # 读取点云
    points, intensities, points_intensities_numpy = read_point_cloud_ply(input_ply)

    # 生成以(xx, yy, zz)为中心的立方体角点
    center = np.array([xx, yy, zz])
    cube_vertices = get_cube_vertices(center, length, width, height)

    # 获取立方体的12条边和6个面
    cube_edges = get_cube_edges(cube_vertices)
    cube_faces = get_cube_faces(cube_vertices)

    # 在每条边上进行插值，生成连接顶点的点，确保插值点的密度一致
    interpolated_points_edges = interpolate_edges(cube_edges, total_points=total_interpolation_points)

    # 在每个面上进行插值，生成覆盖面的点
    interpolated_points_faces = interpolate_faces(cube_faces, total_points=total_interpolation_points*2)

    # 为插值生成的点添加强度值
    interpolated_points_with_intensity_edges = np.zeros((interpolated_points_edges.shape[0], 4))
    interpolated_points_with_intensity_edges[:, :3] = interpolated_points_edges
    interpolated_points_with_intensity_edges[:, 3] = roi_intensities  # 设置边点强度

    interpolated_points_with_intensity_faces = np.zeros((interpolated_points_faces.shape[0], 4))
    interpolated_points_with_intensity_faces[:, :3] = interpolated_points_faces
    interpolated_points_with_intensity_faces[:, 3] = roi_intensities  # 设置面点强度

    # 合并点云、边插值点和面插值点
    new_point_cloud = np.vstack(
        (points_intensities_numpy, interpolated_points_with_intensity_edges, interpolated_points_with_intensity_faces))

    # 保存新的点云
    save_point_cloud_as_ply(new_point_cloud, output_ply)

    print(f"新的点云文件已保存到: {output_ply}")


def ROI_add_to_PLY(pkl_merge):
    # 立方体尺寸

    for root, dirs, files in os.walk(pkl_merge):
        for file in files:
            if file.endswith(".ply"):
                input_ply = os.path.join(root, file)  # 输入文件路径
                # output_ply = os.path.join(root, file.replace(".ply", "_with_cube.ply"))  # 输出文件路径
                output_ply = input_ply # 输出文件路径

                # 立方体尺寸
                xx = carla_config._xx
                yy = carla_config._yy
                zz = carla_config._zz
                xx = carla_config._xx
                length, width, height = carla_config._length, carla_config._width, carla_config._height
                roi_intensities = carla_config._roi_intensities

                # 在点云中添加立方体，指定插值总点数
                add_cube_to_point_cloud_ply(input_ply, output_ply, length, width, height, xx, yy, zz,roi_intensities,
                                            total_interpolation_points=2000)
                # add_cube_to_point_cloud_ply(input_ply, output_ply, 7.94, 2.89, 4.0, 0, 0, 0, roi_intensities,
                #                             total_interpolation_points=1000)
                # add_cube_to_point_cloud_ply(input_ply, output_ply, 9.94, 4.89, 4.0, 0, 0, 0, roi_intensities,
                #                             total_interpolation_points=1000)



                print(f"ROI 处理完成：{input_ply} -> {output_ply}")


# 示例调用
if __name__ == "__main__":
    input_ply = "/home/didi/mmdetection3d_ing/carla_project/CarlaData/mvxnet/mvxnet_pkl_merge/0000008661.ply"  # 输入文件
    output_ply = "/home/didi/mmdetection3d_ing/carla_project/CarlaData/mvxnet/mvxnet_pkl_merge/0000008661_with_cube.ply"  # 输出文件

