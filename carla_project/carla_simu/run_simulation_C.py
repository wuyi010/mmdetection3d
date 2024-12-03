import os
import sys
import glob
import carla
import numpy as np
import cv2
from matplotlib import cm

from carla_project.carla_simu import DisplayManager, get_config_sensor_options, get_config_file_to_transform
from carla_project.carla_simu.CustomTimer import CustomTimer
from carla_project.carla_simu.SensorManager import SensorManager
from carla_project.example.dynamic_weather import set_custom_weather

try:
    sys.path.append(glob.glob('../carla_project/dist/carla_project-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
try:
    import pygame
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_q
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')



def run_simulation(args, client):
    """This function performs one test run using the args parameters
    and connects to the carla_project client passed.
    """
    VIDIDIS = np.array(cm.get_cmap("plasma").colors)
    VID_RANGE = np.linspace(0.0, 1.0, VIDIDIS.shape[0])
    # print("VIDIDIS",VIDIDIS)
    # print(VID_RANGE)

    display_manager = None
    vehicle = None
    vehicle_list = []
    timer = CustomTimer()

    # 获取世界和初始设置
    world = client.load_world('Town04')
    set_custom_weather(world)
    original_settings = world.get_settings()
    # 获取场景中的蓝图
    blueprint_library = world.get_blueprint_library()

    if not args.sync:  # 如果选择非同步模式
        settings = world.get_settings()
        settings.synchronous_mode = False  # 禁用同步模式
        world.apply_settings(settings)

        # 设置观察者视角
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location(x=389.56, y=-224.7, z=15), carla.Rotation(yaw=90)))

    else:  # 同步模式
        traffic_manager = client.get_trafficmanager(args.tm_port)
        settings = world.get_settings()
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.global_percentage_speed_difference(30.0)
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        # 设置观察者视角
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location(x=389.56, y=-224.7, z=15), carla.Rotation(yaw=90)))

    try:
        # 获取spawn点
        spawn_points = world.get_map().get_spawn_points()
        spawn_point_0 = spawn_points[19]

        print(spawn_points)

        # 创建车辆并自动驾驶
        vehicle_bp_hgv = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]
        vehicle_hgv = world.spawn_actor(vehicle_bp_hgv, spawn_point_0)
        vehicle_list.append(vehicle_hgv)
        traffic_manager = client.get_trafficmanager(args.tm_port)  # 管理NPC交通行为8000
        vehicle_hgv.set_autopilot(True,traffic_manager.get_port())
        # vehicle_hgv.set_autopilot(False,traffic_manager.get_port())

        # # 选择路径
        route_1_indices = [65, 16, 283, 26, 31, 317, 371]
        route_1 = [spawn_points[ind].location for ind in route_1_indices]

        # 实例化其他车辆
        spawn_indices = [63, 61, 318, 316, 30, 32, 29, 27, 26, 25, 311, 285, 284, 282, 17, 15, 66, 64]
        vehicle_types = [
            'vehicle.tesla.model3', 'vehicle.tesla.model3', 'vehicle.tesla.model3',
            'vehicle.tesla.model3', 'vehicle.tesla.model3'
        ]

        vehicle_list = spawn_vehicles(world, blueprint_library, spawn_points, vehicle_types, spawn_indices, vehicle_list)



        # 添加传感器并进行配置
        cam_name = [1, 2, 3, 4, 5, 6]
        lidar_name = [1, 2, 3, 4, 5]
        display_rgb_pos = {
            0: [0, 3],
            1: [0, 4],
            2: [0, 1],
            3: [0, 0],
            4: [0, 2]}
        # 创建 LiDAR 映射表
        display_pos_lidar = {
            0: [1, 4],  # L1 对应的位置
            1: [1, 0],  # L2 对应的位置
            2: [1, 3],  # L3 对应的位置
            3: [1, 1],  # L4 对应的位置
            4: [1, 2]  # L5 对应的位置
        }
        display_manager = DisplayManager(grid_size=[2, 5], window_size=[args.width, args.height])

        save_dir = 'config'
        sensor_options_RGBCamera = get_config_sensor_options(os.path.join(save_dir, 'config_sensor_options_RGBCamera.json'))
        sensor_options_LiDAR = get_config_sensor_options(os.path.join(save_dir, 'config_sensor_options_lidar.json'))
        config_rgb = get_config_file_to_transform(os.path.join(save_dir, 'config_rgb.json'))
        config_lidar = get_config_file_to_transform(os.path.join(save_dir, 'config_lidar.json'))

        # 遍历配置并使用映射表设置 display_pos
        for i, transform in enumerate(config_rgb):
            display_pos = display_rgb_pos.get(i, [0, 0])
            SensorManager(world, display_manager, 'RGBCamera',transform,
                          vehicle_hgv, sensor_options_RGBCamera,display_pos, cam_name[i],args)
        # 遍历 LiDAR 传感器配置
        for i, transform in enumerate(config_lidar):
            display_pos = display_pos_lidar.get(i, [1, 0])  # 如果没有匹配则默认[1, 0]
            SensorManager(world, display_manager, 'LiDAR', transform,
                          vehicle_hgv, sensor_options_LiDAR, display_pos,lidar_name[i],args)

        # Simulation loop
        call_exit = False
        # 主循环
        while True:
            # Carla Tick

            if args.sync:
                world.tick()
            else:
                world.wait_for_tick()

            traffic_manager.set_path(vehicle_hgv, route_1)
            # Render received data
            display_manager.render()

            cv2.waitKey(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    call_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        call_exit = True
                        break

            if call_exit:
                break

    except KeyboardInterrupt:
        pass

    finally:
        if display_manager:
            display_manager.destroy()
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicle_list])
        world.apply_settings(original_settings)

        # 恢复设置并清理
        traffic_manager.set_synchronous_mode(False)
        cv2.destroyAllWindows()
        print("All cleaned up!")

def spawn_vehicles(world, blueprint_library, spawn_points,vehicle_types, spawn_indices, vehicle_list):
    try:
        for i, index in enumerate(spawn_indices):
            vehicle_bp = blueprint_library.filter(vehicle_types[i % len(vehicle_types)])[0]
            vehicle = world.spawn_actor(vehicle_bp, spawn_points[index])
            vehicle_list.append(vehicle)
    except Exception as e:
        print(f"Error spawning vehicle: {e}")
    return vehicle_list
