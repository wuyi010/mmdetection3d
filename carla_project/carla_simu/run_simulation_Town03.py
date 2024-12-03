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


def run_simulation_Town03(args, client):
    """This function performs one test run using the args parameters
    and connects to the carla_project client passed.
    """
    VIDIDIS = np.array(cm.get_cmap("plasma").colors)
    VID_RANGE = np.linspace(0.0, 1.0, VIDIDIS.shape[0])

    display_manager = None
    g_vehicle_list = []
    timer = CustomTimer()

    # 获取 Carla 世界和初始设置
    world = client.load_world('Town03')
    set_custom_weather(world)
    original_settings = world.get_settings()  # 保存原始设置

    # 获取蓝图库和同步设置
    blueprint_library = world.get_blueprint_library()

    try:
        if args.sync:  # 同步模式
            print("Setting up synchronous mode...")
            TM = client.get_trafficmanager(args.tm_port)
            TM.set_synchronous_mode(True)  # 设置 TM 为同步模式
            TM.global_percentage_speed_difference(90.0)

            # 设置世界为同步模式
            settings = world.get_settings()
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.1  # 确保 TM 和 Carla 使用相同的时间步长
            world.apply_settings(settings)

            # 设置观察者视角
            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(x=5.854201, y=194.692886, z=8.0), carla.Rotation(yaw=-90.362541)))

        else:  # 非同步模式
            print("Setting up asynchronous mode...")
            TM = client.get_trafficmanager(args.tm_port)
            TM.set_synchronous_mode(False)  # 禁用 TM 同步模式

            # 设置世界为异步模式
            settings = world.get_settings()
            settings.synchronous_mode = False
            world.apply_settings(settings)

            # 设置观察者视角
            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(x=389.56, y=-224.7, z=15), carla.Rotation(yaw=90)))

        # 启动主要的 CARLA 运行逻辑
        main_run_carla(args, client, world, TM, g_vehicle_list,display_manager)

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")

    finally:
        # 清理所有资源
        if display_manager:
            display_manager.destroy()
        client.apply_batch([carla.command.DestroyActor(x) for x in g_vehicle_list])

        # 恢复 Carla 世界的原始设置
        world.apply_settings(original_settings)

        # 恢复 Traffic Manager 的同步模式
        TM.set_synchronous_mode(False)

        # 清理显示器和窗口
        cv2.destroyAllWindows()
        print("All cleaned up!")



def spawn_vehicles_by_type_NPC(world, blueprint_library, spawn_points, vehicle_type_to_indices, g_vehicle_list):
    try:
        # 遍历每种车辆类型及其对应的刷出点
        for vehicle_type, indices in vehicle_type_to_indices.items():
            # 获取车辆蓝图
            vehicle_bp = blueprint_library.filter(vehicle_type)[0]
            for index in indices:
                # 在指定刷出点实例化该类型的车辆
                vehicle = world.spawn_actor(vehicle_bp, spawn_points[index])
                g_vehicle_list.append(vehicle)
                print(f"Spawned {vehicle_type} at spawn point {index}.")
    except Exception as e:
        print(f"Error spawning vehicle: {e}")
    return g_vehicle_list

def spawn_crossbike(world, blueprint_library, g_vehicle_list, vehicle_type,x, y, z=0.281942, yaw=-90.439095):
    """
    生成一辆crossbike并将其添加到车辆列表中。

    参数:
        world: carla世界对象。
        blueprint_library: 车辆蓝图库。
        g_vehicle_list: 存储车辆的列表。
        x, y, z: 车辆的位置坐标 (默认z=0.281942)。
        yaw: 车辆的方向 (默认yaw=90.439095)。
    """
    # 创建车辆的Transform
    vehicle_transform = carla.Transform(carla.Location(x=x, y=y, z=z),
                                        carla.Rotation(pitch=0.000000, yaw=yaw, roll=0.000000))

    # 从蓝图库中选择crossbike蓝图
    crossbike_blueprint = blueprint_library.filter(vehicle_type)[0]

    # 生成车辆
    crossbike = world.spawn_actor(crossbike_blueprint, vehicle_transform)

    # 将生成的车辆加入到g_vehicle_list
    g_vehicle_list.append(crossbike)


import carla
def spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, vehicle_type, x, y, z=0.400000, yaw=-90.439095):
    """
    生成一辆车辆并将其添加到车辆列表中。

    参数:
        world: carla世界对象。
        blueprint_library: 车辆蓝图库。
        g_vehicle_list: 存储车辆的列表。
        vehicle_type: 车辆类型，如 'vehicle.bmw.grandtourer'。
        x, y, z: 车辆的位置坐标 (默认z=0.400000)。
        yaw: 车辆的方向 (默认yaw=90.439095)。
    """
    # 创建车辆的Transform
    vehicle_transform = carla.Transform(carla.Location(x=x, y=y, z=z),
                                        carla.Rotation(pitch=0.000000, yaw=yaw, roll=0.000000))

    # 从蓝图库中选择车辆蓝图
    vehicle_blueprint = blueprint_library.filter(vehicle_type)[0]

    # 生成车辆
    vehicle = world.spawn_actor(vehicle_blueprint, vehicle_transform)

    # 将生成的车辆加入到g_vehicle_list
    g_vehicle_list.append(vehicle)


def main_run_carla(args, client, world, TM, g_vehicle_list,display_manager):
    blueprint_library = world.get_blueprint_library()

    # 获取spawn点
    spawn_points = world.get_map().get_spawn_points()
    # for i, spawn_point in enumerate(spawn_points):    # 在地图上用数字标出刷出点的位置
    #     world.debug.draw_string(spawn_point.location, str(i), life_time=10000000)

        # 定义每种车辆类型和对应的刷出点 indices
    vehicle_type_to_indices = {
        'vehicle.jeep.wrangler_rubicon':    [202],
        'vehicle.tesla.model3':             [39,203,164,38],
        'vehicle.bh.crossbike':             [161],
        'vehicle.ford.mustang':             [160 ],
        'vehicle.toyota.prius':             [ 165],
        'vehicle.gazelle.omafiets':         [37],
        'vehicle.bmw.grandtourer':[40],



    }

    # 调用新的函数进行车辆实例化
    g_vehicle_list = spawn_vehicles_by_type_NPC(world, blueprint_library, spawn_points, vehicle_type_to_indices,
                                            g_vehicle_list)

    """

    前方卡车位置:112  Transform(Location(x=4.997698, y=55.387558, z=0.275307), Rotation(pitch=0.000000, yaw=-88.891235, roll=0.000000))
    前方卡车位置:172  Transform(Location(x=5.854201, y=184.692886, z=0.275307), Rotation(pitch=0.000000, yaw=-90.362541, roll=0.000000))
    x=5.854201, y=184.692886, z=0.275307
    """
    vehicle_type_bwm = 'vehicle.bmw.grandtourer'
    vehicle_positions_bwm = [
        # (1.426758, 184.692886,-90.362541),
        (1.826758, 172.692886, -90.362541),
        # (1.826758, 164.692886, -90.362541),
        # (1.826758, 154.692886, -90.362541),
        # (1.926758, 144.692886, -90.362541),
        # (2.026758, 134.692886, -90.362541),
        # (2.126758, 124.692886, -90.362541),
        # (2.226758, 114.692886, -90.362541),
        (2.326758, 104.692886,  -90.362541),
        # (2.426758, 94.692886,  -90.362541),
        (2.526758, 84.692886,  -90.362541),
        # (2.626758, 74.692886,  -90.362541),
        # (2.7826758, 64.692886,  -90.362541),
        # (2.826758, 54.692886,  -90.362541),

    ]
    vehicle_type_tsl = 'vehicle.tesla.model3'
    vehicle_positions_tsl = [
        # (8.46675,   172.692886,   -90.362541),
        (8.46675,   168.692886,   -90.362541),
        # (8.46675,   154.692886,   -90.062541),
        # (8.46675,   144.692886,   -90.062541),
        # (8.46675,   134.692886,   -90.062541),
        # (8.46675,   124.692886,   -90.362541),
        # (8.46675,   114.692886,   -90.362541),
        (8.46675,   104.692886,   -90.362541),
        (8.46675,   94.692886 ,   -90.362541),
        # (8.46675,   84.692886 ,   -90.362541),
        (8.46675,   74.692886 ,   -90.362541),
        # (8.46675,   64.692886 ,   -90.362541),
        (8.46675,   54.692886 ,   -90.362541),


    ]

    # # 生成车辆并将其加入列表
    for pos in vehicle_positions_bwm:
        spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, vehicle_type_bwm, x=pos[0], y=pos[1],z=0.4000,yaw=pos[2])
    for pos in vehicle_positions_tsl:
        spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, vehicle_type_tsl, x=pos[0], y=pos[1],z=0.4,yaw=pos[2])





    # 自行车 5.854201, y=184.692886, z=0.275307
    spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",3.304201, 161.692886,)
    spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",3.304201, 164.692886,)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",3.304201, 167.692886,)

    spawn_crossbike(world, blueprint_library, g_vehicle_list,"vehicle.kawasaki.ninja",  7.804, 161.692886)
    spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.kawasaki.ninja", 7.804,164.692886)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.kawasaki.ninja", 7.804,167.692886)


    # 前方车辆阻挡视线car_A
    car_A = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]  #8.526758, 164.692886,
    car_A_transform = carla.Transform(carla.Location(x=5.354201, y=149.692886, z=0.281942),
                                      carla.Rotation(pitch=0.000000, yaw=-90.362541, roll=0.000000))
    vehicle_car_A = world.spawn_actor(car_A, car_A_transform)
    g_vehicle_list.append(vehicle_car_A)






    print("前方卡车位置:172 ", spawn_points[172])
    print("前方卡车位置:112 ", spawn_points[112])
    """
    Transform(Location(x=2.354272, y=189.215149, z=0.275307), Rotation(pitch=0.000000, yaw=-90.362541, roll=0.000000))
    """
    vehicle_bp_hgv = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]
    # vehicle_hgv = world.spawn_actor(vehicle_bp_hgv, spawn_points[28])
    car_C_transform = carla.Transform(carla.Location(x=5.354201, y=164.692886, z=0.275307),
                                      carla.Rotation(pitch=0.000000, yaw=-90.362541, roll=0.000000))
    vehicle_hgv = world.spawn_actor(vehicle_bp_hgv, car_C_transform)

    # 获取车辆的碰撞盒（bounding box）
    bounding_box = vehicle_hgv.bounding_box
    extent = bounding_box.extent
    # 打印车辆的尺寸信息
    length = 2 * extent.x  # 长度
    width = 2 * extent.y  # 宽度
    height = 2 * extent.z  # 高度

    print(f"Vehicle dimensions (meters): Length={length:.2f}, Width={width:.2f}, Height={height:.2f}")


    g_vehicle_list.append(vehicle_hgv)
    # vehicle_hgv.set_autopilot(True, TM.get_port())
    vehicle_hgv.set_autopilot(False, TM.get_port())
    # 选择路径
    # route_1_indices = [65, 16, 283, 26, 31, 317, 371]
    # route_1 = [spawn_points[ind].location for ind in route_1_indices]
    # TM.set_path(vehicle_hgv, route_1)
    # vehicle_hgv.set_autopilot(False,TM.get_port())

    # 添加传感器并进行配置
    cam_name = [1, 2, 3, 4, 5, 6]
    lidar_name = [1, 2, 3, 4, 5]
    display_rgb_pos = {0: [0, 3], 1: [0, 4], 2: [0, 1], 3: [0, 0], 4: [0, 2]}
    # 创建 LiDAR 映射表
    display_pos_lidar = {0: [1, 4], 1: [1, 0], 2: [1, 3], 3: [1, 1], 4: [1, 2]}
    display_manager = DisplayManager(grid_size=[2, 5], window_size=[args.width, args.height])

    save_dir = 'config'
    sensor_options_RGBCamera = get_config_sensor_options(os.path.join(save_dir, 'config_sensor_options_RGBCamera.json'))
    sensor_options_LiDAR = get_config_sensor_options(os.path.join(save_dir, 'config_sensor_options_lidar.json'))
    config_rgb = get_config_file_to_transform(os.path.join(save_dir, 'config_rgb.json'))
    config_lidar = get_config_file_to_transform(os.path.join(save_dir, 'config_lidar.json'))

    # 遍历配置并使用映射表设置 display_pos
    for i, transform in enumerate(config_rgb):
        display_pos = display_rgb_pos.get(i, [0, 0])
        SensorManager(world, display_manager, 'RGBCamera', transform,
                      vehicle_hgv, sensor_options_RGBCamera, display_pos, cam_name[i], args)
    # 遍历 LiDAR 传感器配置
    for i, transform in enumerate(config_lidar):
        display_pos = display_pos_lidar.get(i, [1, 0])  # 如果没有匹配则默认[1, 0]
        SensorManager(world, display_manager, 'LiDAR', transform,
                      vehicle_hgv, sensor_options_LiDAR, display_pos, lidar_name[i], args)



    # for i, vehicle in enumerate(g_vehicle_list):
    #     vehicle.set_autopilot(True, TM.get_port())

    # # 列出所有的车辆类型
    # vehicle_types = blueprint_library.filter('vehicle')
    # for vehicle in vehicle_types:
    #     print(vehicle.id)  # 打印车辆类型






    # Simulation loop
    call_exit = False
    while True:
        if args.sync:
            world.tick()
        else:
            world.wait_for_tick()

        # Render received data
        display_manager.render() # 数据呈现: 渲染当前帧的数据（如摄像头图像、LiDAR数据等）

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


