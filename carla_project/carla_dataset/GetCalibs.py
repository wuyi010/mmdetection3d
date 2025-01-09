import os
import pickle
import numpy as np
from carla_project.carla_simu.get_sensor_config import get_config_positions_from_json
from carla_project.carla_tool.draw_points_on_image import draw_points_on_image
from carla_project.carla_tool.transform_Euler_angles_lidar_to_camera import transform_lidar_to_camera, \
    camera_euler_angle_transform
from carla_tool import get_rotation_matrix

"""计算pkl"""
def cam2img_calculate(width,height,fov):
    """
    cam2img: 将相机坐标系中的三维点转换为图像平面上的二维点
    """

    f_x= width / (2 * np.tan(np.radians(float(fov)) / 2))
    f_y = f_x
    c_x, c_y = width / 2, height / 2

    cam2img = np.array([
        [f_x, 0, c_x, 0],
        [0, f_y, c_y, 0],
        [0,   0,   1, 0],
        [0,   0,   0, 1],
    ])
    # cam2img = cam2img[:3, :3]
    return cam2img

def lidar2cam_calculate(location,rotation):
    """
      lidar2cam:
      tx、ty、tz 是平移部分，描述激光雷达坐标系原点到相机坐标系原点的平移。

                      #雷达坐标系：  大拇指指向 x 轴正方向（前方）。
             z    x               食指指向 y 轴正方向（左方）。
             |  /               中指指向 z 轴正方向（上方）。
             | /
       y_____|/
                z      rot_coord_one = np.array([[0, -1, 0],[0, 0, -1],[1, 0, 0]])
               /      相机坐标系
              /
             /_______x
             |
             |
             |
             y
    """
    # 1 carla坐标系原始数据
    carla_x, carla_y, carla_z          = location["x"], location["y"], location["z"],
    carla_pitch, carla_yaw, carla_roll = rotation["pitch"], rotation["yaw"], rotation["roll"]
    # 2 雷达坐标系
    lidar_x,     lidar_y,   lidar_z    = carla_x, -carla_y, carla_z
    lidar_pitch, lidar_yaw, lidar_roll = carla_pitch, -carla_yaw, carla_roll

    R = transform_lidar_to_camera(lidar_pitch, lidar_yaw, lidar_roll)
    T_lidar2cam = R @ np.array([  [lidar_x ],[lidar_y],[lidar_z-2.000] ]) #
    T = -T_lidar2cam

    # 组合平移和旋转以构建 lidar2cam 矩阵
    transformation_matrix = np.zeros((4, 4))
    transformation_matrix[:3, :3] = R
    transformation_matrix[:3, 3] = T.flatten()
    transformation_matrix[3, 3] = 1

    lidar2cam = transformation_matrix
    return lidar2cam



def lidar2img_calculate(cam2img,lidar2cam):
    return np.dot(cam2img, lidar2cam)
if __name__ == '__main__':

    pass
    # CAM_FRONT()
    # CAM_FRONT_RIGHT()
    # CAM_BACK_RIGHT()
    # Location_list = [2, 3, 0, 1, 4]
    # camera_positions_list = ['C3', 'C4', 'C1', 'C2', 'C5']
    # dataset_list_name_list = ['CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK_RIGHT', 'CAM_FRONT',
    #                           "points",
    #                           "calibs", "labels", "ImageSets"]
    #
    #


    # draw_points_on_image(name='000000',
    #                      bin_file_path ='/home/didi/mmdetection3d/data/kitti/testing/velodyne_reduced_all',
    #                      img_file_path ='/home/didi/mmdetection3d/carla_project/Carla_data/dataset/CAM_FRONT_LEFT',
    #                      pkl_file_path ='/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/CAM_FRONT_LEFT',
    #                      )

