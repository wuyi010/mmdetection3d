import json

import carla
import numpy as np
import os
import pickle


from carla_project.carla_simu import get_config_sensor_options, get_config_file_to_transform
from  carla_project.carla_simu import get_config_file_to_transform



config_sensor_options_RGBCamera = {
    "fov": str(90),
    'sensor_tick': str(1),
}
# 定义 LiDAR 配置字典
config_sensor_options_LiDAR = {
    "channels":             str(128),
    "horizontal_fov":       str(120),
    "upper_fov":            str(15),
    "lower_fov":            str(-15),
    "range":                str(100.0),
    "rotation_frequency":   str(20.0),
    "points_per_second":    str(500000),
    "sensor_tick":          str(1)
}
config_sensor_options_LiDAR_1 = {
    "channels":             str(128),
    "horizontal_fov":       str(120),
    "upper_fov":            str(45),
    "lower_fov":            str(-45),
    "range":                str(100.0),
    "rotation_frequency":   str(20.0),
    "points_per_second":    str(500000),
    "sensor_tick":          str(1)
}
config_sensor_options_LiDAR_2 = {
    "channels":             str(128),
    "horizontal_fov":       str(120),
    "upper_fov":            str(12.7),
    "lower_fov":            str(-12.7),
    "range":                str(100.0),
    "rotation_frequency":   str(20.0),
    "points_per_second":    str(500000),
    "sensor_tick":          str(1)
}
config_sensor_options_LiDAR_3 = {
    "channels":             str(128),
    "horizontal_fov":       str(120),
    "upper_fov":            str(45),
    "lower_fov":            str(-45),
    "range":                str(100.0),
    "rotation_frequency":   str(20.0),
    "points_per_second":    str(500000),
    "sensor_tick":          str(1)
}
ego = [0, 0, 0, 7.94, 2.89, 3.46, 0]
# ego = [0, 0, 0, 7.94, 2.60, 3.46, 0]
Location_list =    [ 0, 1,   2,   3,   4,]
camera_positions_list = ['C3', 'C4', 'C1', 'C2', 'C5']
dataset_list_name_list = ['CAM_FRONT_LEFT', 'CAM_BACK_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK_RIGHT', 'CAM_FRONT', "points",
                     "calibs", "labels", "ImageSets"]


"""-----------------------------------------------------   planA  --------------------------------------------------------------"""

# cam_positions_set = [
#             {'location': {'x': 3.45, 'y': 1.37, 'z': 2.1}, 'rotation': {'pitch': -0.0000, 'yaw': 30.0000, 'roll': 0.0000}},  # C1-R45
#             {'location': {'x': 3.45, 'y': 1.37, 'z': 1.9}, 'rotation': {'pitch': 0.0000, 'yaw': 150.0000, 'roll': 0.0000}},  # C2-R135
#             {'location': {'x': 3.45, 'y': -1.37, 'z': 2.1}, 'rotation': {'pitch': 0.0000, 'yaw': -30.0000, 'roll': 0.0000}},  # C3-L45  前右
#             {'location': {'x': 3.45, 'y': -1.37, 'z': 1.9}, 'rotation': {'pitch': 0.0000, 'yaw': -150.0000, 'roll': 0.0000}},  # C4-L135
#             {'location': {'x': 3.8500, 'y': 0.0000, 'z': 2.0}, 'rotation': {'pitch': 0.00, 'yaw': 0.00, 'roll': 0.00}}  # C5-F0H  前
# ]
# lidar_positions_set = [
#     {'location': {'x': 3.450, 'y': 1.5450, 'z': 2.0}, 'rotation': {'pitch': 0.0000, 'yaw': 120.0000, 'roll': 0.0000}},  # L1
#     {'location': {'x': 3.450, 'y': -1.5450, 'z': 2.0}, 'rotation': {'pitch': 0.0000, 'yaw': -120.0000, 'roll': 0.0000}},  # L2
#     {'location': {'x': 0.0000, 'y': 1.44, 'z': 1.8000}, 'rotation': {'pitch': 0.0000, 'yaw': 63.0000, 'roll': 0.0000}},  # L3
#     {'location': {'x': 0.0000, 'y': -1.44, 'z': 1.8000}, 'rotation': {'pitch': 0.0000, 'yaw': -63.0000, 'roll': 0.0000}},  # L4
#     {'location': {'x': 3.8500, 'y': 0.0000, 'z': 1.8000}, 'rotation': {'pitch': 0.0000, 'yaw': 0.0000, 'roll': 0.0000}}  # L5
# ]

"""---------------------------------------------------   planB    -----------------------------------------------------------"""
# # fov=90
# cam_positions_set = [
# {'location': {'x': 3.45, 'y': 1.37, 'z': 2.1}, 'rotation': {'pitch': -17.0, 'yaw': 43.5000, 'roll': 0.0000}},  # C1-R45
# {'location': {'x': 3.45, 'y': 1.37, 'z': 1.95 }, 'rotation': {'pitch': -17.0, 'yaw': 136.5000, 'roll': 0.0}},  # C3-L45  前右
# {'location': {'x': 3.45, 'y': -1.37, 'z': 2.1 }, 'rotation': {'pitch': -17.0, 'yaw': -43.5000, 'roll': 0.0000}},  # C2-R135
# {'location': {'x': 3.45, 'y': -1.37, 'z': 1.95 }, 'rotation': {'pitch': -17.0, 'yaw': -136.5000, 'roll': -0.0}},  # C4-L135
# {'location': {'x': 3.85, 'y': 0.00,  'z': 2.0 }, 'rotation': {'pitch': -10.0, 'yaw': 0.00, 'roll': 0.00}}  # C5-F0H  前
# ]
# #fov=60
# cam_positions_set = [
# {'location': {'x': 3.45, 'y': 1.37, 'z': 2.1}, 'rotation': {'pitch': -10.0, 'yaw': 30.000, 'roll': 0.0000}},  # C1-R45
# {'location': {'x': 3.45, 'y': 1.37, 'z': 1.95 }, 'rotation': {'pitch': -10.0, 'yaw': 150.000, 'roll': 0.0}},  # C3-L45  前右
# {'location': {'x': 3.45, 'y': -1.37, 'z': 2.1 }, 'rotation': {'pitch': -10.0, 'yaw': -30.000, 'roll': 0.0000}},  # C2-R135
# {'location': {'x': 3.45, 'y': -1.37, 'z': 1.95 }, 'rotation': {'pitch': -10.0, 'yaw': -150.000, 'roll': -0.0}},  # C4-L135
# {'location': {'x': 3.85, 'y': 0.00,  'z': 2.0 }, 'rotation': {'pitch': -10.0, 'yaw': 0.00, 'roll': 0.00}}  # C5-F0H  前
# ]
# lidar_positions_set = [
# {'location': {'x': 3.85, 'y': 1.44, 'z': 2.0 }, 'rotation': {'pitch': 0.0000, 'yaw': 45.0, 'roll': 0.0000}}, #右前方
# {'location': {'x': 3.2, 'y': 1.44, 'z': 3.28 }, 'rotation': {'pitch': -50.000, 'yaw': 123.0, 'roll': -27.50}},# 左前方
# {'location': {'x': 3.85, 'y':-1.44, 'z':2.0 }, 'rotation': {'pitch': 0.0000, 'yaw': -45.0, 'roll': 0.0000}},
# {'location': {'x': 3.2, 'y':-1.44, 'z': 3.28 }, 'rotation': {'pitch': -50.00, 'yaw': -123.0, 'roll': 27.5}},
# {'location': {'x': 3.85, 'y': 0.0,  'z': 3.04 }, 'rotation': {'pitch': -45.500, 'yaw': 0.000, 'roll': 0.0000}}
# ]

"""-------------------------------------------------------plan1    ----------------------------------------------------------"""




#不盲雷达：260 304  328
# {'location': {'x': 2.8, 'y': 1.6, 'z': 3.04 }, 'rotation': {'pitch': -45.000, 'yaw': 110.0, 'roll': -20.0}},#      lidar 3
"""--------------------------------------------------------------------------------------------------------------------------"""
#实测3 补盲移动1.6m
cam_positions_set = [
{'location': {'x': 3.55, 'y': 1.30, 'z': 2.0}, 'rotation': {'pitch': -0.0, 'yaw': 45.0000, 'roll': 0.0000}},  # C1-R45
{'location': {'x': 3.55, 'y': 1.30, 'z': 3.28 }, 'rotation': {'pitch': -0.0, 'yaw': 135.0000, 'roll': 0.0}},  # C3-L45  前右
{'location': {'x': 3.55, 'y': -1.30, 'z': 2.0 }, 'rotation': {'pitch': -0.0, 'yaw': -45.0000, 'roll': 0.0000}},  # C2-R135
{'location': {'x': 3.55, 'y': -1.30, 'z': 3.28 }, 'rotation': {'pitch': -0.0, 'yaw': -135.0000, 'roll': -0.0}},  # C4-L135
{'location': {'x': 3.85, 'y': 0.00,  'z': 2.0 }, 'rotation': {'pitch': -0.0, 'yaw': 0.00, 'roll': 0.00}}  # C5-F0H  前
]
lidar_positions_set = [
{'location': {'x': 3.55, 'y': 1.45, 'z': 1.9 }, 'rotation': {'pitch': 0.0000, 'yaw': 30.0, 'roll': 0.0000}}, #AT128 FRONT
{'location': {'x': 3.65, 'y': 1.45, 'z': 1.78 }, 'rotation': {'pitch': -40.5, 'yaw': 149.0, 'roll': -44.0}},# e1 you
{'location': {'x': 3.45, 'y': 1.45, 'z': 1.9 }, 'rotation': {'pitch': 0.0000, 'yaw': 125.0, 'roll': 0.0000}},#AT128 BACK
{'location': {'x': 3.65, 'y':-1.45, 'z': 1.78 }, 'rotation': {'pitch': -34.00, 'yaw': -149.0, 'roll': 47.0}},
{'location': {'x': 3.85, 'y': 0.0,  'z': 2.9 }, 'rotation': {'pitch': -46.000, 'yaw': 0.000, 'roll': 0.0000}}    # FRONT
]



"""--------------------------------------------------   最终方案无死角覆盖    ---------------------------------------------------"""
"""------------------------------------------------x6000---------------------------------------------------------------------------"""
# cam_positions_set = [
# {'location': {'x': 3.7, 'y': 1.45, 'z': 2.0}, 'rotation': {'pitch': -16.0, 'yaw': 45.0000, 'roll': 0.0000}},  # C1-R45
# {'location': {'x': 3.7, 'y': 1.45, 'z': 1.9 }, 'rotation': {'pitch': -16.0, 'yaw': 135.0000, 'roll': 0.0}},  # C3-L45  前右
# {'location': {'x': 3.7, 'y': -1.45, 'z': 2.0 }, 'rotation': {'pitch': -16.0, 'yaw': -45.0000, 'roll': 0.0000}},  # C2-R135
# {'location': {'x': 3.70, 'y': -1.45, 'z': 1.9}, 'rotation': {'pitch': -16.0, 'yaw': -135.0000, 'roll': -0.0}},  # C4-L135
# {'location': {'x': 3.85, 'y': 0.00,  'z': 2.0 }, 'rotation': {'pitch': -10.0, 'yaw': 0.00, 'roll': 0.00}},  # C5-F0H  前
#
# ]
# lidar_positions_set = [
# {'location': {'x': 3.55, 'y': 1.45, 'z': 1.9 }, 'rotation': {'pitch': 0.0000, 'yaw': 30.0, 'roll': 0.0000}}, #AT128 FRONT
# {'location': {'x': 3.55, 'y': 1.45, 'z': 1.78 }, 'rotation': {'pitch': -48.00, 'yaw': 120.0, 'roll': -32.0}},# e1
# {'location': {'x': 3.45, 'y': 1.45, 'z':1.9}, 'rotation': {'pitch': 0.0000, 'yaw': 125.0, 'roll': 0.0000}},#AT128 BACK
# {'location': {'x': 3.55, 'y':-1.45, 'z': 1.78 }, 'rotation': {'pitch': -48.00, 'yaw': -120.0, 'roll': 32.0}},
# {'location': {'x': 3.85, 'y': 0.45,  'z': 3.04 }, 'rotation': {'pitch': -45.000, 'yaw': 0.000, 'roll': 0.0000}}    # FRONT
# ]
"""------------------------------------------------x5000---------------------------------------------------------------------------"""
# cam_positions_set = [
# {'location': {'x': 3.7, 'y': 1.45, 'z': 1.7}, 'rotation': {'pitch': -16.0, 'yaw': 45.0000, 'roll': 0.0000}},  # C1-R45
# {'location': {'x': 3.7, 'y': 1.45, 'z': 1.6 }, 'rotation': {'pitch': -16.0, 'yaw': 135.0000, 'roll': 0.0}},  # C3-L45  前右
# {'location': {'x': 3.7, 'y': -1.45, 'z': 1.7 }, 'rotation': {'pitch': -16.0, 'yaw': -45.0000, 'roll': 0.0000}},  # C2-R135
# {'location': {'x': 3.70, 'y': -1.45, 'z': 1.6}, 'rotation': {'pitch': -16.0, 'yaw': -135.0000, 'roll': -0.0}},  # C4-L135
# {'location': {'x': 3.85, 'y': 0.00,  'z': 2.0 }, 'rotation': {'pitch': -10.0, 'yaw': 0.00, 'roll': 0.00}},  # C5-F0H  前
#
# ]
# lidar_positions_set = [
# {'location': {'x': 3.7, 'y': 1.6, 'z': 1.7 }, 'rotation': {'pitch': 0.0000, 'yaw': 30.0, 'roll': 0.0000}}, #AT128 FRONT
# {'location': {'x': 3.55, 'y': 1.6, 'z': 1.6 }, 'rotation': {'pitch': -48.00, 'yaw': 120.0, 'roll': -32.0}},# e1
# {'location': {'x': 3.65, 'y': 1.6, 'z':1.7 }, 'rotation': {'pitch': 0.0000, 'yaw': 125.0, 'roll': 0.0000}},#AT128 BACK
# {'location': {'x': 3.55, 'y':-1.6, 'z': 1.6 }, 'rotation': {'pitch': -48.00, 'yaw': -120.0, 'roll': 32.0}},
# {'location': {'x': 3.85, 'y': 0.0,  'z': 3.04 }, 'rotation': {'pitch': -45.000, 'yaw': 0.000, 'roll': 0.0000}}    # FRONT
# ]
"""------------------------------------------------x TEST---------------------------------------------------------------------------"""
"""---------------------------------------------------------------------------------------------------------------------------"""



cam_positions = [
    carla.Transform(
        carla.Location(pos['location']['x'], pos['location']['y'], pos['location']['z']),
        carla.Rotation(pos['rotation']['pitch'], pos['rotation']['yaw'], pos['rotation']['roll'])
    )
    for pos in cam_positions_set
]

lidar_positions = [
    carla.Transform(
        carla.Location(
            pos['location']['x'],
            pos['location']['y'],
            pos['location']['z']   # 这里对 z 值减去 2
        ),
        carla.Rotation(
            pos['rotation']['pitch'],
            pos['rotation']['yaw'],
            pos['rotation']['roll']
        )
    )
    for pos in lidar_positions_set
]




# 转换成字典
transform_dicts_cam = [{
                        'location': {
                            'x': transform.location.x,
                            'y': transform.location.y,
                            'z': transform.location.z
                        },
                        'rotation': {
                            'pitch': transform.rotation.pitch,
                            'yaw': transform.rotation.yaw,
                            'roll': transform.rotation.roll
                        }
                    } for transform in cam_positions]

# 转换成字典
transform_dicts_lidar = [{
                        'location': {
                            'x': transform.location.x,
                            'y': transform.location.y,
                            'z': transform.location.z
                        },
                        'rotation': {
                            'pitch': transform.rotation.pitch,
                            'yaw': transform.rotation.yaw,
                            'roll': transform.rotation.roll
                        }
                    } for transform in lidar_positions]




def config_save_to_json(save_dir):
    """
    保存配置文件到指定路径
    :param save_dir: 保存文件的路径目录
    """
    # 确保目录存在，不存在则创建
    os.makedirs(save_dir, exist_ok=True)

    # 保存为 JSON 文件
    with open(os.path.join(save_dir, 'config_rgb.json'), 'w') as f:
        json.dump(transform_dicts_cam, f, indent=4)

    with open(os.path.join(save_dir, 'config_lidar.json'), 'w') as f:
        json.dump(transform_dicts_lidar, f, indent=4)

    # 将字典保存为 JSON 文件
    with open(os.path.join(save_dir, 'config_sensor_options_lidar.json'), 'w') as f:
        json.dump(config_sensor_options_LiDAR, f, indent=4)
    with open(os.path.join(save_dir, 'config_sensor_options_lidar_1.json'), 'w') as f:
        json.dump(config_sensor_options_LiDAR_1, f, indent=4)
    with open(os.path.join(save_dir, 'config_sensor_options_lidar_2.json'), 'w') as f:
        json.dump(config_sensor_options_LiDAR_2, f, indent=4)
    with open(os.path.join(save_dir, 'config_sensor_options_lidar_3.json'), 'w') as f:
        json.dump(config_sensor_options_LiDAR_3, f, indent=4)

    with open(os.path.join(save_dir, 'config_sensor_options_RGBCamera.json'), 'w') as f:
        json.dump(config_sensor_options_RGBCamera, f, indent=4)


def get_sensor_cfg():
    print("cam_positions：", cam_positions)
    print("lidar_positions：", lidar_positions)
    save_dir = 'config'

    config_save_to_json(save_dir)

    get_config_sensor_options(os.path.join(save_dir, 'config_sensor_options_lidar.json'))
    get_config_sensor_options(os.path.join(save_dir, 'config_sensor_options_RGBCamera.json'))
    config_rgb = get_config_file_to_transform(    os.path.join(save_dir, 'config_rgb.json'))
    config_lidar = get_config_file_to_transform( os.path.join(save_dir, 'config_lidar.json'))


if __name__ == '__main__':
    get_sensor_cfg()
    # main_carla()







