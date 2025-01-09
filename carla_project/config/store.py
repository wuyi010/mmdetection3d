# Server configuration
import os

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
CarlaDataPath = dict(
    dataset_path='CarlaData/',
    camera_path ='CarlaData/Camera/',
    lidar_path  ='CarlaData/Lidar/',
    #更新
    #MVXNetDataset set
    mvxnet_path_name ='CarlaData/mvxnet/',
    mvxnet_pkl_merge='CarlaData/mvxnet/mvxnet_pkl_merge',
    mvxnet_pkl_file='CarlaData/mvxnet/dataset.pkl',
    mvxnet_bin_folder='CarlaData/mvxnet/LidarBin',
    mvxnet_cal_folder='CarlaData/mvxnet/Calibs',
    mvxnet_out_folder='CarlaData/mvxnet/Output',

    # BEVFusionDataset set
    bevfusion_path_name='CarlaData/bevfusion/',
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
config_cam = config_cam_R9x16e2_f60
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
    "upper_fov":                str(15),   # 上半部分垂直视场角为12.7°
    "lower_fov":                str(-15.0),  # 下半部分垂直视场角为-12.7°
    "range":                    str(200.0),  # 探测距离200米@10%反射率
    "rotation_frequency":       str(10),     # 转速为10Hz
    "points_per_second":        str(1536000), # 每秒153.6万点
    "sensor_tick":              str(1)       # 1秒钟一次的采样
}

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
config_SemanticLiDAR = config_SemanticLiDAR_n128_120x30_m200_f10_pps1b53w

CamName_base = ['CAM_FRONT','CAM_FRONT_LEFT', 'CAM_FRONT_RIGHT','CAM_BACK_LEFT', 'CAM_BACK_RIGHT','CAM_BACK']
#方案A--------------------------------------------------------
SensorCamera_set1 = {
    'CAM_FRONT':       {'config':config_cam, 'location': {'x': 3.85, 'y': 0.00,  'z': 2.00}, 'rotation': {'pitch': -0.00, 'yaw': 0.00,   'roll': 0.00}},
    'CAM_FRONT_LEFT':  {'config':config_cam, 'location': {'x': 0.0, 'y': 1.37,  'z': 2.10}, 'rotation': {'pitch': -0.00, 'yaw': 30.00,  'roll': 0.00}},
    'CAM_FRONT_RIGHT': {'config':config_cam, 'location': {'x': 0.0, 'y': -1.37, 'z': 2.10}, 'rotation': {'pitch': -0.00, 'yaw': -30.00, 'roll': 0.00}},
    'CAM_BACK_LEFT':   {'config':config_cam, 'location': {'x': 3.55, 'y': 1.37, 'z': 1.90}, 'rotation': {'pitch': -0.00, 'yaw': 150.00,'roll': 0.00}},
    'CAM_BACK_RIGHT':  {'config':config_cam, 'location': {'x': 3.55, 'y': -1.37,  'z': 1.90}, 'rotation': {'pitch': -0.00, 'yaw': -150.00, 'roll': 0.00}},
    'CAM_BACK':        {'config':config_cam, 'location': {'x': -3.85, 'y': 0.00, 'z': 2.00}, 'rotation': {'pitch': -0.00, 'yaw':  -180.00, 'roll': 0.00}}, }
SensorLiDAR_set1 = {
    'CAM_FRONT':      {'config': config_LiDAR, 'location': {'x':3.85, 'y': 0.0000, 'z': 1.80}, 'rotation': {'pitch': 0.00, 'yaw': 0.00,   'roll': 0.00}},
    'CAM_FRONT_LEFT': {'config': config_LiDAR,'location': {'x': 0.0, 'y': -1.44,  'z': 1.80},   'rotation': {'pitch': 0.00, 'yaw': -63.00, 'roll': 0.00}},
    'CAM_FRONT_RIGHT':{'config': config_LiDAR,'location': {'x': 0.0, 'y': 1.44,  'z': 1.80},  'rotation': {'pitch': 0.00, 'yaw': 63.00, 'roll': 0.00}},
    'CAM_BACK_LEFT':  {'config': config_LiDAR,'location': {'x': 3.55, 'y': -1.54, 'z': 2.0}, 'rotation': {'pitch': 0.00, 'yaw': -120.00, 'roll': 0.00}},
    'CAM_BACK_RIGHT': {'config': config_LiDAR,'location': {'x': 3.55, 'y': 1.54, 'z': 2.0},    'rotation': {'pitch': 0.00, 'yaw': 120.00, 'roll': 0.00}},
    'CAM_BACK':       {'config': config_LiDAR,'location': {'x': -3.85, 'y': 0.00 , 'z': 2.0},     'rotation': {'pitch': 0.00, 'yaw': 180.00, 'roll': 0.00}},}
#方案B--------------------------------------------------------
# fov=90 cam
# cam_positions_set = [
# {'location': {'x': 3.45, 'y': 1.37, 'z': 2.1}, 'rotation': {'pitch': -17.0, 'yaw': 43.5000, 'roll': 0.0000}},  # C1-R45
# {'location': {'x': 3.45, 'y': 1.37, 'z': 1.95 }, 'rotation': {'pitch': -17.0, 'yaw': 136.5000, 'roll': 0.0}},  # C3-L45  前右
# {'location': {'x': 3.45, 'y': -1.37, 'z': 2.1 }, 'rotation': {'pitch': -17.0, 'yaw': -43.5000, 'roll': 0.0000}},  # C2-R135
# {'location': {'x': 3.45, 'y': -1.37, 'z': 1.95 }, 'rotation': {'pitch': -17.0, 'yaw': -136.5000, 'roll': -0.0}},  # C4-L135
# {'location': {'x': 3.85, 'y': 0.00,  'z': 2.0 }, 'rotation': {'pitch': -10.0, 'yaw': 0.00, 'roll': 0.00}}  # C5-F0H  前
# ]
# fov=60 cam
SensorCamera_set2 = {
    'CAM_FRONT':{'config':config_cam, 'location': {'x': 3.85, 'y': 0.00,  'z': 2.00}, 'rotation': {'pitch': -10.00, 'yaw': 0.00,   'roll': 0.00}},
    'CAM_FRONT_RIGHT':{'config':config_cam, 'location': {'x': 3.45, 'y': 1.37,  'z': 2.10}, 'rotation': {'pitch': -10.00, 'yaw': 30.00,  'roll': 0.00}},
    'CAM_FRONT_LEFT':{'config':config_cam, 'location': {'x': 3.45, 'y': -1.37, 'z': 2.10}, 'rotation': {'pitch': -10.00, 'yaw': -30.00, 'roll': 0.00}},
    'CAM_BACK_RIGHT':{'config':config_cam, 'location': {'x': 3.45, 'y': 1.37, 'z': 1.95}, 'rotation': {'pitch': -10.00, 'yaw': 150.00,'roll': 0.00}},
    'CAM_BACK_LEFT':{'config':config_cam, 'location': {'x': 3.45, 'y': -1.37,  'z': 1.95}, 'rotation': {'pitch': -10.00, 'yaw': -150.00, 'roll': 0.00}},
    'CAM_BACK':{'config':config_cam, 'location': {'x': -3.85, 'y': 0.00, 'z': 2.00}, 'rotation': {'pitch': -10.00, 'yaw':  -180.00, 'roll': 0.00}}, }
SensorLiDAR_set2 = {
'CAM_FRONT'         :{'config': config_LiDAR, 'location': {'x':3.85, 'y': 0.0000, 'z': 3.04},'rotation': {'pitch': -45.00, 'yaw': 0.00,   'roll': 0.00}},
'CAM_FRONT_LEFT'    :{'config': config_LiDAR,'location': {'x': 3.85, 'y': -1.44,  'z': 2.0}, 'rotation': {'pitch':-0.00,   'yaw': -45.00, 'roll': 0.00}},
'CAM_FRONT_RIGHT'   :{'config': config_LiDAR,'location': {'x': 3.85, 'y': 1.44,  'z': 2.0},  'rotation': {'pitch': 0.00,   'yaw': 45.00, 'roll': 0.00}},
'CAM_BACK_LEFT'     :{'config': config_LiDAR,'location': {'x': 3.2, 'y': -1.44, 'z': 3.28},  'rotation': {'pitch': -50.0,  'yaw': -123.00,'roll': 27.5}},
'CAM_BACK_RIGHT'    :{'config': config_LiDAR,'location': {'x': 3.2, 'y': 1.44, 'z': 3.28},   'rotation': {'pitch': -50.00, 'yaw': 123.00, 'roll':-27.5}},
'CAM_BACK'          :{'config': config_LiDAR,'location': {'x': -3.85, 'y': 0.00 , 'z': 3.04},'rotation': {'pitch': 0.00,   'yaw': 180.00, 'roll': 0.00}},}

SensorCamera_set3 = {
    'CAM_FRONT':       {'config':config_cam, 'location': {'x': 3.85, 'y': 0.00,  'z': 2.00}, 'rotation': {'pitch': -10.00, 'yaw': 0.00,   'roll': 0.00}},
    'CAM_FRONT_LEFT':  {'config':config_cam, 'location': {'x': 3.45, 'y': 1.45,  'z': 2.10}, 'rotation': {'pitch': -16.00, 'yaw': 45.00,  'roll': 0.00}},
    'CAM_FRONT_RIGHT': {'config':config_cam, 'location': {'x': 3.45, 'y': -1.45, 'z': 2.10}, 'rotation': {'pitch': -16.00, 'yaw': -45.00, 'roll': 0.00}},
    'CAM_BACK_LEFT':   {'config':config_cam, 'location': {'x': 3.45, 'y': 1.45, 'z': 1.95}, 'rotation': {'pitch': -16.00, 'yaw': 135.00,'roll': 0.00}},
    'CAM_BACK_RIGHT':  {'config':config_cam, 'location': {'x': 3.45, 'y': -1.45,  'z': 1.95}, 'rotation': {'pitch': -16.00, 'yaw': -135.00, 'roll': 0.00}},
    'CAM_BACK':        {'config':config_cam, 'location': {'x': -3.85, 'y': 0.00, 'z': 2.00}, 'rotation': {'pitch': -10.00, 'yaw':  -180.00, 'roll': 0.00}}, }
SensorLiDAR_set3 = {
    'CAM_FRONT':      {'config': config_LiDAR, 'location': {'x':3.85, 'y': 0.0000, 'z': 3.04},'rotation': {'pitch': -45.00, 'yaw': 0.00,   'roll': 0.00}},
    'CAM_FRONT_LEFT': {'config': config_LiDAR,'location': {'x': 3.55, 'y': -1.44,  'z': 2.0}, 'rotation': {'pitch':-0.00,   'yaw': -45.00, 'roll': 0.00}},
    'CAM_FRONT_RIGHT':{'config': config_LiDAR,'location': {'x': 3.85, 'y': 1.44,  'z': 2.0},  'rotation': {'pitch': 0.00,   'yaw': 45.00, 'roll': 0.00}},
    'CAM_BACK_LEFT':  {'config': config_LiDAR,'location': {'x': 3.2, 'y': -1.44, 'z': 3.28},  'rotation': {'pitch': -48.0,  'yaw': -123.00,'roll': 18.}},
    'CAM_BACK_RIGHT': {'config': config_LiDAR,'location': {'x': 3.2, 'y': 1.44, 'z': 3.28},   'rotation': {'pitch': -48.00, 'yaw': 123.00, 'roll':-18.}},
    'CAM_BACK':       {'config': config_LiDAR,'location': {'x': -3.85, 'y': 0.00 , 'z': 3.04},'rotation': {'pitch': 0.00,   'yaw': 180.00, 'roll': 0.00}},}

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



#生成选择方案
SensorCameraName = [name for name in SensorCamera_set2]
SensorLiDARName =  [name for name in SensorLiDAR_set2]
print("SensorCamera_Name:",SensorCameraName)
print("SensorLiDAR_Name:",SensorLiDARName)

Selection_simulation_environment = 4  # 执行run_simulation_Town04
SensorCamera_set = SensorCamera_set2
SensorLiDAR_set = SensorLiDAR_set2






