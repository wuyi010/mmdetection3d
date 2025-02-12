# Server configuration
# 获取当前工作目录 (即运行脚本时的目录)
import numpy as np

Server = {
    'host': '127.0.0.1',
    'port': 2000,
    'tm_port': 8000,
    'sync': True,
}
World = {
    'global_percentage_speed_difference': 90,
    'worldSettingsSynchronous_mode' :True,
    'fixed_delta_seconds' :0.1,
    "set_vehicle_list_autopilot" :False,# 自动驾驶使能
}
# Carla data paths configuration
# 生成相对于当前工作目录的路径
# CarlaDataPath = {
#     'dataset_path': os.path.join(base_dir, 'CarlaData'),  # 将文件夹创建在当前工作目录下
#     'camera_path': os.path.join(base_dir, 'CarlaData', 'Camera'),
#     'lidar_path': os.path.join(base_dir, 'CarlaData', 'Lidar'),
# }

CarlaDataPath = dict(
    dataset_path='CarlaData/',
    camera_path='CarlaData/Camera',
    lidar_path='CarlaData/Lidar',
    #更新
    #MVXNetDataset set
    mvxnet_path_name ='CarlaData/mvxnet',
    mvxnet_pkl_merge='CarlaData/mvxnet/mvxnet_pkl_merge',
    mvxnet_pkl_file='CarlaData/mvxnet/dataset.pkl',
    mvxnet_bin_folder='CarlaData/mvxnet/LidarBin',
    mvxnet_cal_folder='CarlaData/mvxnet/Calibs',
    mvxnet_out_folder='CarlaData/mvxnet/Output',

    # BEVFusionDataset set
    bevfusion_path_name='CarlaData/bevfusion',
    bevfusion_pkl_merge='CarlaData/bevfusion/bevfusion_pkl_merge',
    bevfusion_pkl_folder='CarlaData/bevfusion/dataset.pkl',
    bevfusion_camera_folder='CarlaData/bevfusion/Camera',
    bevfusion_bin_folder='CarlaData/bevfusion/LidarBin',
    bevfusion_cal_folder='CarlaData/bevfusion/Calibs',
    bevfusion_out_folder='CarlaData/bevfusion/Output',
)

EgoSize = [0, 0, 0, 7.94, 2.89, 3.46, 0]
"""# Sensor Camera configuration"""
DisplayWindows ={'H':800,'W':1800}
Res900x1600  = {'H': 900,'W': 1600}
Res1080x1920 = {'H': 1080,'W': 1920}
config_cam_R9x16e2_f60 = { 'resolution':Res900x1600, 'options':{"fov": str(60), 'sensor_tick': str(1)},}
config_cam_R9x16e2_f90 = { 'resolution':Res900x1600, 'options':{"fov": str(90), 'sensor_tick': str(1)},}
config_cam = config_cam_R9x16e2_f90
"""# Sensor iDAR configuration"""
config_LiDAR_old = {'dropoff_general_rate':0.45,'dropoff_intensity_limit': 0,'dropoff_zero_intensity':0.4, "channels":str(128),
                    "horizontal_fov": str(120),"upper_fov": str(15), "lower_fov":str(-15), "range":str(150.0),
                    "rotation_frequency":str(20.0),"points_per_second":str(1530000),"sensor_tick":str(1)}
config_LiDAR_n128_120x30_m200_f10_pps1b53w = {
    'dropoff_general_rate':     str(0.0),    # 强度衰减一般速率为0
    'dropoff_intensity_limit':  str(0.0),    # 强度衰减上限为0
    'dropoff_zero_intensity':   str(0.0),    # 无强度时的衰减为0
    "channels":                 str(128),    # 通道数128
    "horizontal_fov":           str(120),    # 水平视场角120°
    "upper_fov":                str(15),     # 上半部分垂直视场角为12.7°
    "lower_fov":                str(-15.0),  # 下半部分垂直视场角为-12.7°
    "range":                    str(200.0),  # 探测距离200米@10%反射率
    "rotation_frequency":       str(10),     # 转速为10Hz
    "points_per_second":        str(1036000), # 每秒153.6万点
    "sensor_tick":              str(1)       # 1秒钟一次的采样
}
# "points_per_second":        str(1536000), # 每秒153.6万点

config_SemanticLiDAR_n128_120x30_m200_f10_pps1b53w = {
    'role_name': 'SemanticLiDAR',
    "channels":                 str(128),    # 通道数128
    "horizontal_fov":           str(120),    # 水平视场角120°
    "upper_fov":                str(15),   # 上半部分垂直视场角为12.7°
    "lower_fov":                str(-15.0),  # 下半部分垂直视场角为-12.7°
    "range":                    str(200.0),  # 探测距离200米@10%反射率
    "rotation_frequency":       str(10),     # 转速为10Hz
    "points_per_second":        str(1536000), # 每秒153.6万点
    "sensor_tick":              str(1)       # 1秒钟一次的采样
}
config_LiDAR_n128_120x25_4_m200_f10_pps1b53w = {
    'dropoff_general_rate':     str(0.0),
    'dropoff_intensity_limit':  str(0.0),
    'dropoff_zero_intensity':   str(0.0),
    "channels":                 str(128),  # AT128本身就是128通道，保持不变
    "horizontal_fov":           str(120),  # 水平视场角120°，保持不变
    "upper_fov":                str(12.7),  # 垂直视场角为25.4°，取一半即上半部分为12.7°
    "lower_fov":                str(12.7),  # 对应下半部分为-12.7°
    "range":                    str(200.0),  # 探测距离200米@10%反射率，修改为200
    "rotation_frequency":       str(10),  # 假设转速为10Hz（具体可按实际情况调整）
    "points_per_second":        str(1536000),  # 单回波每秒153.6万点，这里按准确数值填写
    "sensor_tick":              str(1)
}
config_LiDAR_n128_120x45_m200_f10_pps1b53w = {
    'dropoff_general_rate':     str(0.0),    # 强度衰减一般速率为0
    'dropoff_intensity_limit':  str(0.0),    # 强度衰减上限为0
    'dropoff_zero_intensity':   str(0.0),    # 无强度时的衰减为0
    "channels":                 str(128),    # 通道数128
    "horizontal_fov":           str(120),    # 水平视场角120°
    "upper_fov":                str(45.0),   # 上半部分垂直视场角为12.7°
    "lower_fov":                str(-45.0),  # 下半部分垂直视场角为-12.7°
    "range":                    str(200.0),  # 探测距离200米@10%反射率
    "rotation_frequency":       str(10),     # 转速为10Hz
    "points_per_second":        str(1536000), # 每秒153.6万点
    "sensor_tick":              str(1)       # 1秒钟一次的采样
}


config_LiDAR = config_LiDAR_n128_120x30_m200_f10_pps1b53w
# config_LiDAR = config_LiDAR_n128_120x45_m200_f10_pps1b53w
config_SemanticLiDAR = config_SemanticLiDAR_n128_120x30_m200_f10_pps1b53w


#方案A--------------------------------------------------------




# SensorCamera_set1 = dict(#fov=60
# CAM_FRONT      = {'config':config_cam, 'location': {'x': 3.85, 'y': 0.00,  'z': 2.00}, 'rotation': {'pitch': -0.00, 'yaw': 0.00,   'roll': 0.00}},
# CAM_FRONT_LEFT = {'config':config_cam, 'location': {'x': 3.45, 'y': -1.37, 'z': 2.10}, 'rotation': {'pitch': -0.00, 'yaw': -30.00, 'roll': 0.00}},
# CAM_FRONT_RIGHT= {'config':config_cam, 'location': {'x': 3.45, 'y': 1.37,  'z': 2.10}, 'rotation': {'pitch': -0.00, 'yaw': 30.00,  'roll': 0.00}},
# CAM_BACK_LEFT  = {'config':config_cam, 'location': {'x': 3.45, 'y': -1.37,  'z': 1.90}, 'rotation': {'pitch': -0.00, 'yaw': -150.00, 'roll': 0.00}},
# CAM_BACK_RIGHT ={'config':config_cam, 'location': {'x': 3.45, 'y': 1.37, 'z': 1.90}, 'rotation': {'pitch': -0.00, 'yaw': 150.00,'roll': 0.00}},
# CAM_BACK       = {'config':config_cam, 'location': {'x': -3.85, 'y': 0.00, 'z': 2.00}, 'rotation': {'pitch': -0.00, 'yaw':  -180.00, 'roll': 0.00}},
# )
SensorCamera_set1 = dict( #fov=90
CAM_FRONT      = {'config':config_cam, 'location': {'x': 3.85, 'y': 0.00,  'z': 2.0}, 'rotation': {'pitch': -0.00, 'yaw': 0.00,   'roll': 0.00}},
CAM_FRONT_LEFT = {'config':config_cam, 'location': {'x': 3.55, 'y': -1.40, 'z': 2.0}, 'rotation': {'pitch': 0.00, 'yaw': -45.0, 'roll': 0.00}},
CAM_FRONT_RIGHT= {'config':config_cam, 'location': {'x': 3.55, 'y': 1.40,  'z': 2.0}, 'rotation': {'pitch': 0.00, 'yaw': 45.0,  'roll': 0.00}},
CAM_BACK_LEFT  = {'config':config_cam, 'location': {'x': 3.55, 'y': -1.40,  'z': 1.9}, 'rotation': {'pitch': -0.00, 'yaw': -135.00, 'roll': 0.00}},
CAM_BACK_RIGHT = {'config':config_cam, 'location': {'x': 3.55, 'y': 1.40, 'z': 1.9}, 'rotation':  {'pitch': -0.00, 'yaw': 135.00,'roll': 0.00}},
# CAM_BACK       = {'config':config_cam, 'location': {'x': -2.00, 'y': 2.4, 'z': 1.2}, 'rotation': {'pitch': -0.00, 'yaw':  -90.00, 'roll': 0.00}},
# CAM_BACK       = {'config':config_cam, 'location': {'x': 0.00, 'y': -1.440, 'z': 8}, 'rotation': {'pitch': -90.00, 'yaw':  0.00, 'roll': 0.00}},
)
SensorLiDAR_set1 = dict(
CAM_FRONT      = {'config': config_LiDAR,'location': {'x': 3.85, 'y': 0.0000, 'z': 1.4}, 'rotation': {'pitch': 0.00, 'yaw': 0.00,   'roll': 0.00}},
CAM_FRONT_LEFT = {'config': config_LiDAR,'location': {'x': 3.55, 'y': -1.4,  'z': 2.0},  'rotation': {'pitch': 0.00, 'yaw': -63.00, 'roll': 0.00}},
CAM_FRONT_RIGHT= {'config': config_LiDAR,'location': {'x': 3.55, 'y': 1.4,  'z': 2.0},   'rotation': {'pitch': 0.00, 'yaw': 63.00, 'roll': 0.00}},
CAM_BACK_LEFT  = {'config': config_LiDAR,'location': {'x': 3.55, 'y': -1.545, 'z': 2.0},    'rotation': {'pitch': 0.00, 'yaw': -120.00, 'roll': 0.00}},
CAM_BACK_RIGHT = {'config': config_LiDAR,'location': {'x': 3.55, 'y': 1.545, 'z': 2.0},    'rotation': {'pitch': 0.00, 'yaw': 120.00, 'roll': 0.00}},
)
#方案B--------------------------------------------------------
"""左边负的 逆时针为负 右边正的 carla左边是副的"""
# SensorCamera_set2 = dict(# fov=60 cam
# CAM_FRONT      = {'config':config_cam, 'location': {'x': 3.85, 'y': 0.00,  'z': 2.00}, 'rotation': {'pitch': -10.00, 'yaw': 0.00,   'roll': 0.00}},
# CAM_FRONT_LEFT = {'config':config_cam, 'location': {'x': 3.45, 'y': -1.37, 'z': 2.10}, 'rotation': {'pitch': -10.00, 'yaw': -30.00, 'roll': 0.00}},
# CAM_FRONT_RIGHT= {'config':config_cam, 'location': {'x': 3.45, 'y': 1.37,  'z': 2.10}, 'rotation': {'pitch': -10.00, 'yaw': 30.00,  'roll': 0.00}},
# CAM_BACK_LEFT  = {'config':config_cam, 'location': {'x': 3.45, 'y': -1.37,  'z': 1.95}, 'rotation': {'pitch': -10.00, 'yaw': -150.00, 'roll': 0.00}},
# CAM_BACK_RIGHT = {'config':config_cam, 'location': {'x': 3.45, 'y': 1.37, 'z': 1.95}, 'rotation': {'pitch': -10.00, 'yaw': 150.00,'roll': 0.00}},
# CAM_BACK       = {'config':config_cam, 'location': {'x': -3.85, 'y': 0.00, 'z': 2.00}, 'rotation': {'pitch': -10.00, 'yaw':  -180.00, 'roll': 0.00}},
# )
SensorCamera_set2 = dict(# fov=90 cam
CAM_FRONT      = {'config':config_cam, 'location': {'x': 3.85, 'y': 0.00,  'z': 2.00}, 'rotation': {'pitch': -10.00, 'yaw': 0.00,   'roll': 0.00}},
CAM_FRONT_LEFT = {'config':config_cam, 'location': {'x': 3.45, 'y': -1.40, 'z': 2.00}, 'rotation': {'pitch': -12.00, 'yaw': -45.0, 'roll': 0.00}},
CAM_FRONT_RIGHT= {'config':config_cam, 'location': {'x': 3.45, 'y': 1.40,  'z': 2.00}, 'rotation': {'pitch': -12.00, 'yaw': 45.0,  'roll': 0.00}},
CAM_BACK_LEFT  = {'config':config_cam, 'location': {'x': 3.45, 'y': -1.40, 'z': 2.0}, 'rotation': {'pitch': -24.00, 'yaw': -135.0, 'roll': 0.00}},
CAM_BACK_RIGHT = {'config':config_cam, 'location': {'x': 3.45, 'y': 1.40,  'z': 2.0}, 'rotation': {'pitch': -24.00,  'yaw':   135.0,'roll': 0.00}},
# CAM_BACK       = {'config':config_cam, 'location': {'x': 2.0 , 'y': 1.4, 'z': 4.0}, 'rotation': {'pitch': -90.00, 'yaw':  -90.00, 'roll': 0.00}},

)
"""左负 逆时针负 右正  """
SensorLiDAR_set2 = dict(
CAM_FRONT        ={'config': config_LiDAR, 'location': {'x': 3.85,  'y': 0.00, 'z': 3.0}, 'rotation': {'pitch': -48.00, 'yaw': 0.00,    'roll': 0.00}},
CAM_FRONT_LEFT   ={'config': config_LiDAR, 'location': {'x': 3.55, 'y': -1.45,  'z': 2.0},  'rotation': {'pitch':-10.00,  'yaw': -48.00,   'roll': 0.00}},
CAM_FRONT_RIGHT  ={'config': config_LiDAR, 'location': {'x': 3.55, 'y': 1.45,  'z': 2.0}, 'rotation': {'pitch': -10.00,   'yaw': 48.00,  'roll': 0.00}},
CAM_BACK_LEFT    ={'config': config_LiDAR, 'location': {'x': 0.8, 'y': -1.45, 'z': 4.0},  'rotation': {'pitch': -65.0,  'yaw': -116.00,  'roll': 24}},
CAM_BACK_RIGHT   ={'config': config_LiDAR, 'location': {'x': 0.8, 'y': 1.45,  'z': 4.0 }, 'rotation': {'pitch': -65.00, 'yaw': 116.00, 'roll':-24}},
)
# 3.28

_xx, _yy, _zz, _length, _width, _height, _roi_intensities = 10, 0, 0, 40.0, 11.25, 4, 1

#生成选择方案
set='B' # B A
if set=='A':
    SensorCamera_set = SensorCamera_set1
    SensorLiDAR_set = SensorLiDAR_set1
else: #B
    SensorCamera_set = SensorCamera_set2
    SensorLiDAR_set = SensorLiDAR_set2
SensorCameraName = [name for name in SensorCamera_set]
SensorLiDARName =  [name for name in SensorLiDAR_set]
# 根据 SensorLiDARName 的长度生成一个从 0 到 1 的等间隔的序列
intensity_values = np.linspace(0, 1, len(SensorLiDARName))
# 创建字典，按顺序将强度值映射到传感器
sensor_intensity_map = {SensorLiDARName[i]: intensity_values[i] for i in range(len(SensorLiDARName))}
Selection_simulation_environment = 10  # 执行run_simulation_Town04 3 4 10
Layered_display = False
Layered_display = True #会引起mvxnet识别错误






