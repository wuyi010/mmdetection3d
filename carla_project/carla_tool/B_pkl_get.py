import os
import pickle
import numpy as np

from carla_project.A0_config import config_sensor_options_RGBCamera
from carla_project.carla_simu import parse_arguments
from carla_project.carla_simu.sensor_config import get_config_positions_from_json
from carla_project.carla_tool.draw_points_on_image import draw_points_on_image
from carla_project.carla_tool.transform_Euler_angles_lidar_to_camera import transform_lidar_to_camera

"""计算pkl"""
def cam2img_calculate(width,height,fov):
    """
    cam2img: 将相机坐标系中的三维点转换为图像平面上的二维点
    """
    print("图像宽高视场: (", width, height, fov, ")")
    f_x= width / (2 * np.tan(np.radians(float(fov)) / 2))
    f_y = f_x
    c_x, c_y = width / 2, height / 2
    print("f_x, f_y,c_x, c_y: ", f_x, f_y,c_x, c_y  )
    cam2img = np.array([
        [f_x, 0, c_x, 0],
        [0, f_y, c_y, 0],
        [0,   0,   1, 0],
        [0,   0,   0, 1],
    ])
    return cam2img


def lidar2cam_calculate(index,cam_positions_file="../carla_project/config/config_rgb.json"):
    """
    lidar2cam:
    将激光雷达坐标系中的三维点转换到相机坐标系。
    这个矩阵通常包含激光雷达和相机之间的位置和方向的变换。
    lidar2cam = [[r11, r12, r13, tx],
                [r21, r22, r23, ty],
                [r31, r32, r33, tz],
                [0,   0,   0,  1]]`
    rij 是旋转部分，描述激光雷达坐标系到相机坐标系的旋转。
    tx、ty、tz 是平移部分，描述激光雷达坐标系原点到相机坐标系原点的平移。
    """

    # 平移部分，假设相机位置已知（这里使用示例值）
    cam_positions = get_config_positions_from_json(cam_positions_file )
    location = cam_positions[index]['location']
    rotation = cam_positions[index]['rotation']
    T_x, T_y, T_z, pitch, yaw, roll = location["x"], location["y"], location["z"],rotation["pitch"], rotation["yaw"], rotation["roll"]
    print( "T_x,  T_y,  T_z, pitch, yaw, roll: ",T_x, T_y, T_z, pitch, yaw, roll)


    # 计算旋转矩阵
    R = transform_lidar_to_camera(pitch, yaw, roll)
    # 平移向量
    """
    T_x   T_y  T_z  = [3.85  0.   2.8 ]
    T_x   T_y  T_z  = [3.85  0.   2.8 ]
    T= R @ np.array([[T_x], [T_y], [T_z]])
    X Y Z = [[ 0.  ][-2.8 ][ 3.85]]
    """
    # x,y, z = -T_x ,-T_y, -T_z
    # t = -np.array([[0],
    #                [2.8],
    #                [3.85]])

    cam_positions_transfor = R @ np.array([[T_x  ],[T_y ],[T_z-2.000  ]])
    move = -cam_positions_transfor
    print(move)
    # move[0][0]=0
    # move[1][0]=0
    # move[2][0]=0
    # move[2][0]=-3

    print("平移向量: \n",move)
    # 组合平移和旋转以构建 lidar2cam 矩阵
    transformation_matrix = np.zeros((4, 4))
    transformation_matrix[:3, :3] = R
    transformation_matrix[:3, 3] = move.flatten()
    transformation_matrix[3, 3] = 1

    lidar2cam = transformation_matrix
    return lidar2cam

def generate_pkg_single_file(save_pkg_file="None",sample_id=None, img_path_name_=None, lidar_path_=None,
                            cam2img_=None,lidar2cam_=None,Tr_velo_to_cam_=None, lidar2img_ = None,width= None,height= None):
    # 获取文件夹路径
    folder_path = os.path.dirname(save_pkg_file)
    # 如果目录不存在，创建该目录
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    data = {'metainfo': {'DATASET': 'KITTI'},
     'data_list': [{'sample_id': sample_id,
                    'images': {'CAM2': {'img_path': img_path_name_,
                                        'height': height,
                                        'width': width,
                                        'cam2img': cam2img_,
                                        'lidar2cam': lidar2cam_,
                                        'lidar2img': lidar2img_   },
                               'R0_rect': [[1, 0, 0, 0],[0, 1, 0, 0], [0, 0, 1, 0],[0, 0, 0, 1]]},
                    'lidar_points': {'num_pts_feats': 4,
                                     'lidar_path': lidar_path_,
                                     'Tr_velo_to_cam': Tr_velo_to_cam_,
                                     # 'Tr_imu_to_velo': [ [0.999997615814209, 0.0007553070900030434, -0.002035825978964567,-0.8086758852005005],[-0.0007854027207940817, 0.9998897910118103, -0.014822980388998985, 0.3195559084415436],[0.002024406101554632, 0.014824540354311466, 0.9998881220817566,-0.7997230887413025], [0.0, 0.0, 0.0, 1.0]]
                                     },
                    }]}


    with open(save_pkg_file, 'wb') as f:
        pickle.dump(data, f)
        # pickle.dump(data_sourse_use, f)
    print(f"{sample_id}", end="->")  # 输出后不换行





from carla_project.A0_config import  camera_positions_list, dataset_list_name_list,Location_list
def generate_pkl(args):
    cam_positions_file = "/home/didi/mmdetection3d/carla_project/config/config_rgb.json"
    point_folder_path = '/home/didi/mmdetection3d/carla_project/Carla_data/dataset/points'
    # Location_list = [2, 3, 0, 1, 4]
    camera2dataset = dict(zip(Location_list[:5], dataset_list_name_list[:5]))
    print(camera2dataset)
    for position,name in camera2dataset.items():
        # Location =    [ 2,                3,               0,                 1,                 4,]
        # camera_id   = ['C3',             'C4',            'C1',              'C2',             'C5']
        # dataset_son = ['CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK_RIGHT', 'CAM_FRONT']
        width, height, = args.IM_WIDTH, args.IM_HEIGHT
        fov = config_sensor_options_RGBCamera["fov"]
        cam2img = cam2img_calculate(width, height, fov)
        lidar2cam = lidar2cam_calculate(position, cam_positions_file)
        lidar2img = cam2img @ lidar2cam
        FILE_NAME = name
        # 获取文件数量

        file_count = len([name for name in os.listdir(point_folder_path) if os.path.isfile(os.path.join(point_folder_path, name))])
        for i in range(file_count):
            file_name = f'{i:06d}'
            generate_pkg_single_file(
                save_pkg_file=f"/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/{FILE_NAME}/{file_name}.pkl",
                sample_id=i,
                img_path_name_=f"{file_name}.png",
                lidar_path_=f"{file_name}.bin",
                cam2img_=cam2img,
                lidar2cam_=lidar2cam,  # 新的 lidar2cam_ 参数
                Tr_velo_to_cam_=lidar2cam,  # 新的 Tr_velo_to_cam_ 参数
                lidar2img_=lidar2img,
                width=width,
                height=height,
            )
        print(f"保存 {FILE_NAME}完毕")


def CAM_FRONT():
    FILE_NAME = "CAM_FRONT"
    print("\n相机内参：", )

    index= 4
    width, height, = args.IM_WIDTH, args.IM_HEIGHT
    fov =  config_sensor_options_RGBCamera["fov"]
    cam_positions_file= "/home/didi/mmdetection3d/carla_project/config/config_rgb.json"

    cam2img = cam2img_calculate(width, height, fov)
    lidar2cam = lidar2cam_calculate(index, cam_positions_file)
    lidar2img = cam2img @ lidar2cam

    print("相机内参 cam2img**：\n",cam2img)
    print("雷达相机,lidar2cam**：\n", lidar2cam)
    print("lidar2img:\n", lidar2img)

    for i in range(31):
        file_name = f'{i:06d}'
        generate_pkg_single_file(
                save_pkg_file  =   f"/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/{FILE_NAME}/{file_name}.pkl",
                sample_id      =    i,
                img_path_name_ =    f"{file_name}.png",
                lidar_path_    =    f"{file_name}.bin",
                cam2img_       =    cam2img,
                lidar2cam_     =    lidar2cam,      # 新的 lidar2cam_ 参数
                Tr_velo_to_cam_=    lidar2cam ,# 新的 Tr_velo_to_cam_ 参数
                 lidar2img_    =    lidar2img,
                         width = width,
                        height = height,
            )
    print(f"保存 {FILE_NAME}完毕")
def CAM_FRONT_RIGHT():
    FILE_NAME = "CAM_FRONT_RIGHT"
    print("\n相机内参：", )

    index= 2
    width, height, = args.IM_WIDTH, args.IM_HEIGHT
    fov =  config_sensor_options_RGBCamera["fov"]
    cam_positions_file= "/home/didi/mmdetection3d/carla_project/config/config_rgb.json"

    cam2img = cam2img_calculate(width, height, fov)
    lidar2cam = lidar2cam_calculate(index, cam_positions_file)
    lidar2img = cam2img @ lidar2cam

    print("相机内参 cam2img**：\n",cam2img)
    print("雷达相机,lidar2cam**：\n", lidar2cam)
    print("lidar2img:\n", lidar2img)

    for i in range(31):
        file_name = f'{i:06d}'
        generate_pkg_single_file(
                save_pkg_file  =   f"/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/{FILE_NAME}/{file_name}.pkl",
                sample_id      =    i,
                img_path_name_ =    f"{file_name}.png",
                lidar_path_    =    f"{file_name}.bin",
                cam2img_       =    cam2img,
                lidar2cam_     =    lidar2cam,      # 新的 lidar2cam_ 参数
                Tr_velo_to_cam_=    lidar2cam ,# 新的 Tr_velo_to_cam_ 参数
                 lidar2img_    =    lidar2img,
                         width = width,
                        height = height,
            )
    print(f"保存 {FILE_NAME}完毕")
def CAM_BACK_RIGHT():
    FILE_NAME = "CAM_BACK_RIGHT"
    print("\n相机内参：", )

    index= 3
    width, height, = args.IM_WIDTH, args.IM_HEIGHT
    fov =  config_sensor_options_RGBCamera["fov"]
    cam_positions_file= "/home/didi/mmdetection3d/carla_project/config/config_rgb.json"

    cam2img = cam2img_calculate(width, height, fov)
    lidar2cam = lidar2cam_calculate(index, cam_positions_file)
    lidar2img = cam2img @ lidar2cam

    print("相机内参 cam2img**：\n",cam2img)
    print("雷达相机,lidar2cam**：\n", lidar2cam)
    print("lidar2img:\n", lidar2img)

    for i in range(31):
        file_name = f'{i:06d}'
        generate_pkg_single_file(
                save_pkg_file  =   f"/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/{FILE_NAME}/{file_name}.pkl",
                sample_id      =    i,
                img_path_name_ =    f"{file_name}.png",
                lidar_path_    =    f"{file_name}.bin",
                cam2img_       =    cam2img,
                lidar2cam_     =    lidar2cam,      # 新的 lidar2cam_ 参数
                Tr_velo_to_cam_=    lidar2cam ,# 新的 Tr_velo_to_cam_ 参数
                 lidar2img_    =    lidar2img,
                         width = width,
                        height = height,
            )
    print(f"保存 {FILE_NAME}完毕")
def CAM_FRONT_LEFT():
    FILE_NAME = "CAM_FRONT_LEFT"
    print("\n相机内参：", )

    index= 3
    width, height, = args.IM_WIDTH, args.IM_HEIGHT
    fov =  config_sensor_options_RGBCamera["fov"]
    cam_positions_file= "/home/didi/mmdetection3d/carla_project/config/config_rgb.json"

    cam2img = cam2img_calculate(width, height, fov)
    lidar2cam = lidar2cam_calculate(index, cam_positions_file)
    lidar2img = cam2img @ lidar2cam

    print("相机内参 cam2img**：\n",cam2img)
    print("雷达相机,lidar2cam**：\n", lidar2cam)
    print("lidar2img:\n", lidar2img)

    for i in range(31):
        file_name = f'{i:06d}'
        generate_pkg_single_file(
                save_pkg_file  =   f"/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/{FILE_NAME}/{file_name}.pkl",
                sample_id      =    i,
                img_path_name_ =    f"{file_name}.png",
                lidar_path_    =    f"{file_name}.bin",
                cam2img_       =    cam2img,
                lidar2cam_     =    lidar2cam,      # 新的 lidar2cam_ 参数
                Tr_velo_to_cam_=    lidar2cam ,# 新的 Tr_velo_to_cam_ 参数
                 lidar2img_    =    lidar2img,
                         width = width,
                        height = height,
            )
    print(f"保存 {FILE_NAME}完毕")


if __name__ == '__main__':
    args = parse_arguments()
    generate_pkl(args)
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
    draw_points_on_image(name='000000',
                         bin_file_path ='/home/didi/mmdetection3d/data/kitti/testing/velodyne_reduced_all',
                         img_file_path ='/home/didi/mmdetection3d/carla_project/Carla_data/dataset/CAM_FRONT_LEFT',
                         pkl_file_path ='/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/CAM_FRONT_LEFT',
                         )

