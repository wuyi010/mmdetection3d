
import os
import sys
import glob
import carla
import numpy as np
import cv2
from matplotlib import cm
from config import carla_config
from carla_example.dynamic_weather import set_custom_weather
from carla_project.carla_simu import DisplayManager
from carla_project.carla_simu.Asimu import SensorManager, CustomTimer

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


def run_simulation_CARGO(client):
    """This function performs one test run using the args parameters
    and connects to the carla_project client passed.
    """
    VIDIDIS = np.array(cm.get_cmap("plasma").colors)
    VID_RANGE = np.linspace(0.0, 1.0, VIDIDIS.shape[0])

    display_manager = None
    g_vehicle_list = []
    timer = CustomTimer()

    # 获取 Carla 世界和初始设置
    world = client.load_world('Town04')
    set_custom_weather(world)
    original_settings = world.get_settings()  # 保存原始设置

    # 获取蓝图库和同步设置
    blueprint_library = world.get_blueprint_library()

    try:
        if carla_config.Server["sync"]:  # 同步模式
            print("Setting up synchronous mode...")
            TM = client.get_trafficmanager(carla_config.Server["tm_port"])
            TM.set_synchronous_mode(True)  # 设置 TM 为同步模式
            TM.global_percentage_speed_difference(90.0)

            # 设置世界为同步模式
            settings = world.get_settings()
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.1  # 确保 TM 和 Carla 使用相同的时间步长
            world.apply_settings(settings)

            # 设置观察者视角
            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(x=389.56, y=-134.7, z=15), carla.Rotation(yaw=90)))

        else:  # 非同步模式
            print("Setting up asynchronous mode...")
            TM = client.get_trafficmanager(carla_config.Server["tm_port"])
            TM.set_synchronous_mode(False)  # 禁用 TM 同步模式

            # 设置世界为异步模式
            settings = world.get_settings()
            settings.synchronous_mode = False
            world.apply_settings(settings)

            # 设置观察者视角
            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(x=389.56, y=-224.7, z=15), carla.Rotation(yaw=90)))

        # 启动主要的 CARLA 运行逻辑
        main_run_carla(world, TM, g_vehicle_list)

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

def spawn_crossbike(world, blueprint_library, g_vehicle_list, vehicle_type,x, y, z=0.281942, yaw=90.439095):
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



def spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, vehicle_type, x, y, z=0.400000, yaw=90.439095,pitch=0,roll=0):
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
                                        carla.Rotation(pitch=pitch, yaw=yaw, roll=roll))

    # 从蓝图库中选择车辆蓝图
    vehicle_blueprint = blueprint_library.filter(vehicle_type)[0]

    # 生成车辆
    vehicle = world.spawn_actor(vehicle_blueprint, vehicle_transform)

    # 将生成的车辆加入到g_vehicle_list
    g_vehicle_list.append(vehicle)


def main_run_carla(world, TM, g_vehicle_list):
    blueprint_library = world.get_blueprint_library()

    print("_______________________")
    # 获取所有车辆类型
    blueprints_vehicles = world.get_blueprint_library().filter('vehicle.*')
    # 获取所有行人类型
    blueprints_walkers = world.get_blueprint_library().filter('walker.pedestrian.*')
    # # 列出所有的车辆类型
    # vehicle_types = blueprint_library.filter('vehicle')
    # for vehicle in vehicle_types:
    #     print(vehicle.id)  # 打印车辆类型

    # # 按字符串输出所有行人类型
    # walker_types = [walker.id for walker in blueprints_walkers]
    # for walker_type in walker_types:
    #     print(walker_type)

    print("_______________________")

    """显示可刷出车辆位置"""
    spawn_points = world.get_map().get_spawn_points()
    # for i, spawn_point in enumerate(spawn_points):    # 在地图上用数字标出刷出点的位置
    #     world.debug.draw_string(spawn_point.location, str(i), life_time=10000000)

    """获取实际刷出位置"""
    print("前方卡车位置:317 ", spawn_points[317])

    """非主场景车辆"""
    # 定义每种车辆类型和对应的刷出点 indices
    vehicle_type_to_indices = {
        # 'vehicle.jeep.wrangler_rubicon':    [46],
        # 'vehicle.tesla.model3':             [51,314,44,366],
        # 'vehicle.bh.crossbike':             [52,49,312, 45],
        # 'vehicle.ford.mustang':             [50, 315, ],
        # 'vehicle.toyota.prius':             [ 48, 39,],
        # 'vehicle.volkswagen.t2':            [ 33, ],
        # 'vehicle.gazelle.omafiets':         [51,],
        # 'vehicle.bmw.grandtourer':[311],
    }
    g_vehicle_list = spawn_vehicles_by_type_NPC(world, blueprint_library, spawn_points, vehicle_type_to_indices,g_vehicle_list)

    """车辆刷新场景分布"""
    vehicle_positions = [
        # # (381.481506, -154.471375,  90),
        # (vehicle_type_bwm, 381.481506, -144.471375, 90),
        #
        # # (vehicle_type_bwm, 381.481506, -134.471375,  100),
        # (vehicle_type_bwm, 381.481506, -124.471375, 90),
        # (vehicle_type_bwm, 381.481506, -114.471375, 90),
        # # (vehicle_type_bwm, 381.481506, -104.471375,   90),
        #   (vehicle_type_bwm, 381.481506, -94.471375, 90),
        # # (vehicle_type_bwm, 381.681506, -84.471375 ,   90),
        # # (vehicle_type_bwm, 381.481506, -74.471375 ,   90),
        #   (vehicle_type_bwm, 381.481506, -54.471375, 90),

        # (tsl,394.481506,  -134.471375,  90),
        # (tsl,394.481506,  -124.471375,  90),
        # (tsl,394.481506,  -114.471375,  90),
        # (tsl,394.481506,  -104.471375,  90),
        # (tsl,394.481506,  -94.471375 ,  90),
        # (tsl,394.281506,  -84.471375 ,   90),
        # (tsl,394.481506,  -74.471375 ,   90),
        # (tsl,394.481506,  -64.471375 ,   90),
        # (tsl,394.481506, -54.471375 ,   90),
        # (tsl,394.481506,  -44.471375 , 90),
        # (tsl,391.481506, -84.471375, 90),

        # (tsl,385.481506, -74.471375, 90),
        # (tsl,385.481506, -84.471375, 90),


        # (tsl,386.481506, -130.444522, 90),  #盲区夹角
        # (tsl,384.481506, -130.471375, 0),  #盲区夹角
        # (tsl,378.481506, -128.471375, 90),  #盲区夹角

        # ego=（395.15，127）
        # 右侧车头贴近车身盲区位置和车尾位置
        # 1.车辆前方和侧方，贴近车身的位置，放置一些小孩模型（没有小孩就用大人）；【截图2张照片】
        ("walker.pedestrian.0013", 395.15,    -122.9,  90),     # 盲区 车宽 395.15-1.445 =393.705 +0.2m
        ("walker.pedestrian.0013", 393.505,   -123.0,  90),     # 盲区 车宽 395.15-1.445 =393.705 +0.2m
        ("walker.pedestrian.0013", 393.505,   -127.0,  90),     # 盲区 车宽 395.15-1.445 =393.705 +0.2m
        ("walker.pedestrian.0013", 393.505,   -131.0, 90),      # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03

        # # 前方、右侧邻近车道内：小孩行人 摩托车 自行车
        # 2.车辆前方和侧方，车道边缘的位置，放置一些小孩模型（没有小孩就用大人）；【截图2张照片】
        ("walker.pedestrian.0013", 395.15,    -118.0, 90),  # 盲区 车宽 395.15-1.445 =393.705 +0.2m
        ("vehicle.kawasaki.ninja", 392.005,   -118.0, 90),      # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        ("walker.pedestrian.0013", 392.005,   -123.0, 90),      # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        ("vehicle.kawasaki.ninja", 392.005,   -127.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        ('vehicle.bh.crossbike',   392.005,   -131.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03

        #3.相邻车道，车辆侧前方、侧方、侧后方，各放置一台小轿车；【截图1张照片】
        # ('vehicle.tesla.model3', 392.005, -114.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        # ('vehicle.jeep.wrangler_rubicon', 392.005, -123.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        # ('vehicle.tesla.model3', 392.005, -132.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03

        # 4.相邻车道，车辆侧前方、侧方、侧后方，各放置一台卡车；【截图1张照片】
        # ('vehicle.carlamotors.european_hgv', 391.005, -114.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        # ('vehicle.carlamotors.european_hgv', 391.005, -127.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        # ('vehicle.carlamotors.european_hgv', 391.005, -136.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03

        # ('vehicle.tesla.model3', 387.15, -123.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03

        # 5.最右侧车道，车辆侧前方、侧方、侧后方，各放置一台小轿车；【截图1张照片】
        # ('vehicle.tesla.model3',             383.15, -114.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        # ('vehicle.jeep.wrangler_rubicon',    383.15, -123.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        # ('vehicle.tesla.model3',             383.15, -132.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03

        # 6.最右侧车道，车辆侧前方、侧方、侧后方，各放置一台卡车；【截图1张照片】
        ('vehicle.carlamotors.european_hgv', 384.45, -112.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        ('vehicle.carlamotors.european_hgv', 384.45, -121.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
        ('vehicle.carlamotors.european_hgv', 384.45, -130.0, 90),  # 盲区 车长 3.97  127 +-3.97 = 130.97  123.03
    ]

    # 一堵墙
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-142.0, z=5.0, yaw=90, pitch=90, roll=90)
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-138.0, z=5.0, yaw=90, pitch=90, roll=90)
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-134.0, z=5.0, yaw=90,pitch=90, roll=90)
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-130.0, z=5.0, yaw=90,pitch=90, roll=90)
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-126.0, z=5.0, yaw=90, pitch=90, roll=90)
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-122.0, z=5.0, yaw=90, pitch=90, roll=90)
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-118.0, z=5.0, yaw=90, pitch=90, roll=90)
    # spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, "vehicle.carlamotors.european_hgv",
    #                        x=387.15, y=-114.0, z=5.0, yaw=90, pitch=90, roll=90)
    for pos in vehicle_positions:
        spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, pos[0], x=pos[1], y=pos[2],z=0.281942,yaw=pos[3])

    """ego左侧自行车布置"""
    # # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",x=390.681506, y=-136.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",x=390.681506, y=-133.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",x=390.681506, y=-130.417725)

    """ego右侧摩托车布置"""
    # # spawn_crossbike(world, blueprint_library, g_vehicle_list,"vehicle.kawasaki.ninja", x=386.281506, y=-136.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.kawasaki.ninja", x=386.281506, y=-133.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.kawasaki.ninja", x=386.281506, y=-130.417725)

    """ego前方卡车布置"""
    # car_A = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]
    # car_A_transform = carla.Transform(carla.Location(x=388.481506, y=-119.445007, z=0.281942),carla.Rotation(pitch=0.000000, yaw=90.439095, roll=0.000000))
    # vehicle_car_A = world.spawn_actor(car_A, car_A_transform)
    # g_vehicle_list.append(vehicle_car_A)

    """ego布置"""
    vehicle_bp_hgv = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]
    # vehicle_hgv = world.spawn_actor(vehicle_bp_hgv, spawn_points[28])
    car_C_transform = carla.Transform(carla.Location(x=395.15, y=-127.0, z=0.281942),
                                      carla.Rotation(pitch=0.000000, yaw=90.439095, roll=0.000000))
    vehicle_hgv = world.spawn_actor(vehicle_bp_hgv, car_C_transform)
    print("ego vehicle_hgv position: ",spawn_points[28])


    """ego车辆size获取"""#获取车辆的碰撞盒（bounding box）
    bounding_box = vehicle_hgv.bounding_box
    extent = bounding_box.extent
    # 打印车辆的尺寸信息
    length = 2 * extent.x  # 长度
    width = 2 * extent.y  # 宽度
    height = 2 * extent.z  # 高度
    print(f"Vehicle dimensions (meters): Length={length:.2f}, Width={width:.2f}, Height={height:.2f}")

    """ego车辆自动驾驶设置"""
    g_vehicle_list.append(vehicle_hgv)
    # vehicle_hgv.set_autopilot(True, TM.get_port())
    vehicle_hgv.set_autopilot(False, TM.get_port())
    # 选择路径
    route_1_indices = [65, 16, 283, 26, 31, 317, 371]
    route_1 = [spawn_points[ind].location for ind in route_1_indices]
    TM.set_path(vehicle_hgv, route_1)
    # vehicle_hgv.set_autopilot(False,TM.get_port())

    """ego车辆传感器配置"""

    display_manager = DisplayManager(grid_size=[2, 5], window_size=[carla_config.DisplayWindows['W'],carla_config.DisplayWindows['H']])
    display_rgb_pos = {0: [0, 1], 1: [0, 0], 2: [0, 2],
                       3: [1, 0], 4: [1, 2], 5: [1, 1]}
    display_lidar_pos = {0: [0, 4], 1: [0, 3], 2: [0, 5],
                         3: [1, 3], 4: [1, 5], 5: [1, 4]}
    for i, (cam_name, camera_data) in enumerate(carla_config.SensorCamera_set.items()):
        # 提取位置和旋转信息
        location = camera_data['location']
        rotation = camera_data['rotation']

        # 格式化为 Transform 格式
        transform = carla.Transform(
            carla.Location(x=location['x'], y=location['y'], z=location['z']),
            carla.Rotation(pitch=rotation['pitch'], yaw=rotation['yaw'], roll=rotation['roll'])
        )
        # 提取传感器选项
        sensor_options = camera_data['config']['options']
        print("生成",cam_name,"选择参数sensor_options: ",sensor_options)

        # 执行 SensorManager
        SensorManager(world=world,
                      display_man=display_manager,
                      sensor_type='RGBCamera',
                      transform=transform,
                      attached=vehicle_hgv,
                      sensor_options=sensor_options,
                      display_pos=display_rgb_pos.get(i),
                      sensor_name=cam_name,)
    for i, (LiDARName, LiDARData) in enumerate(carla_config.SensorLiDAR_set.items()):
        # 提取位置和旋转信息
        location = LiDARData['location']
        rotation = LiDARData['rotation']

        # 格式化为 Transform 格式
        transform = carla.Transform(
            carla.Location(x=location['x'], y=location['y'], z=location['z']),
            carla.Rotation(pitch=rotation['pitch'], yaw=rotation['yaw'], roll=rotation['roll'])
        )
        # 提取传感器选项
        sensor_options = LiDARData['config']
        print("生成", LiDARName, "选择参数sensor_options: ", sensor_options)

        # 执行 SensorManager
        SensorManager(world=world,
                      display_man=display_manager,
                      sensor_type='LiDAR',
                      # sensor_type='SemanticLiDAR',
                      transform=transform,
                      attached=vehicle_hgv,
                      sensor_options=sensor_options,
                      display_pos=display_lidar_pos.get(i),
                      sensor_name=LiDARName,)

    # Simulation loop
    call_exit = False
    while True:
        if carla_config.Server["sync"]:
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

