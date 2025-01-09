import os
import sys
import glob
import carla
import numpy as np
import cv2
from matplotlib import cm
from carla_project.carla_example.dynamic_weather import set_custom_weather, set_rain_snow_weather, set_rain_fog_weather, \
    set_night_rain_snow_weather
from carla_project.carla_simu.Asimu import SensorManager, DisplayManager, CustomTimer
from config import carla_config

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
def run_simulation_Town04(client):
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
    # set_rain_snow_weather(world)
    set_rain_fog_weather(world)
    # set_night_rain_snow_weather(world)

    original_settings = world.get_settings()  # 保存原始设置

    # 获取蓝图库和同步设置
    blueprint_library = world.get_blueprint_library()

    try:
        if carla_config.Server["sync"]:  # 同步模式
            print("Setting up synchronous mode...")
            TM = client.get_trafficmanager(carla_config.Server["tm_port"])
            TM.set_synchronous_mode(carla_config.Server["sync"])  # 设置 TM 为同步模式
            TM.global_percentage_speed_difference(carla_config.World["global_percentage_speed_difference"])

            # 设置世界为同步模式
            settings = world.get_settings()
            settings.synchronous_mode =carla_config.World["worldSettingsSynchronous_mode"]
            settings.fixed_delta_seconds =carla_config.World["fixed_delta_seconds"]  # 确保 TM 和 Carla 使用相同的时间步长
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
        main_run_carla(client, world, TM, g_vehicle_list,display_manager)

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



def spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, vehicle_type, x, y, z, yaw=90.439095):
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


def main_run_carla(client, world, TM, g_vehicle_list,display_manager):
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
    print("前方卡车位置:48 ", spawn_points[48])
    print("前方卡车位置:47 ", spawn_points[47])
    print("前方卡车位置:46 ", spawn_points[46])
    print("前方卡车位置:45 ", spawn_points[45])
    print("前方卡车位置:43 ", spawn_points[43])
    """
前方卡车位置:48  Transform(Location(x=413.002808, y=-122.528442, z=0.281942), Rotation(pitch=0.000000, yaw=-89.401421, roll=0.000000))
前方卡车位置:47  Transform(Location(x=409.525055, y=-124.664810, z=0.281942), Rotation(pitch=0.000000, yaw=-89.401421, roll=0.000000))
前方卡车位置:46  Transform(Location(x=406.003143, y=-122.601570, z=0.281942), Rotation(pitch=0.000000, yaw=-89.401421, roll=0.000000))
前方卡车位置:45  Transform(Location(x=402.525452, y=-124.737938, z=0.281942), Rotation(pitch=0.000000, yaw=-89.401421, roll=0.000000))
前方卡车位置:43  Transform(Location(x=409.784119, y=-149.469055, z=0.281942), Rotation(pitch=0.000000, yaw=-89.401421, roll=0.000000))

    """

    """非主场景车辆"""
    # 定义每种车辆类型和对应的刷出点 indices
    vehicle_type_to_indices = {
        'vehicle.carlamotors.european_hgv': [44, 48, ],
        'vehicle.tesla.model3': [47, 43,45,33,281,15],
        'vehicle.ford.mustang': [46],
        'vehicle.toyota.prius': [42, ],
        'vehicle.bh.crossbike': [286],
        'vehicle.bmw.grandtourer':[17,49],
    }

    """车辆刷新场景分布"""
    vehicle_positions = [
        #隔壁车道车辆
        # ('vehicle.carlamotors.european_hgv', 409.525055, -128.601570, -89.401421),  # 47号
        # ('vehicle.carlamotors.european_hgv', 413.003143, -149.601570, -100.401421),  # 42号

        ('vehicle.jeep.wrangler_rubicon',    401.525452, -108.601570, 0.8, -100.401421),  # 45
        ('vehicle.jeep.wrangler_rubicon',    405.525452, -116.601570, 0.8, -95.401421),  # 45
        ( 'vehicle.jeep.wrangler_rubicon',   406.525452, -128.601570, 0.8, -98.401421),  # 45
        ('vehicle.bmw.grandtourer',          408.481506, -140.471375, 0.8, -86.401421),
        # 隔壁车道车辆

        # (381.481506, -154.471375,  90),
        ('vehicle.bmw.grandtourer', 392.481506, -162.471375,   0.3,  90),
        # ('vehicle.bmw.grandtourer', 381.481506, -174.471375,   0.3, 90),
        ('vehicle.bmw.grandtourer', 381.481506, -164.471375,   0.3, 90),
        ('vehicle.bmw.grandtourer', 381.481506, -144.471375,   0.3, 90),
        ('vehicle.bmw.grandtourer', 381.481506, -124.471375,   0.3, 90),
        ('vehicle.bmw.grandtourer', 381.481506, -104.471375,   0.3,  90),
        ('vehicle.bmw.grandtourer', 381.481506, -84.471375,    0.3,  90),

        ('vehicle.tesla.model3',391.081506,   -102.471375, 0.5, 90),
        ('vehicle.tesla.model3',385.281506,   -102.471375,  0.5,90),


        # ('vehicle.bh.crossbike',  378.281506,    -124.471375, 0.281942, 90),
        # ('walker.pedestrian.0029',377.481506,   -138.071375,  90),
        # ('walker.pedestrian.0029',377.481506,   -145.471375,  0.5,90),
        # ('walker.pedestrian.0029',377.881506,   -150.871375,  0.5, 0),




    ]
    for pos in vehicle_positions:
        spawn_vehicle_side_two(world, blueprint_library, g_vehicle_list, pos[0], x=pos[1], y=pos[2],z=pos[3],yaw=pos[4])

    """ego左侧自行车布置"""
    # # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",x=390.681506, y=-136.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",x=390.681506, y=-133.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.bh.crossbike",x=390.681506, y=-130.417725)

    """ego右侧摩托车布置"""
    # # spawn_crossbike(world, blueprint_library, g_vehicle_list,"vehicle.kawasaki.ninja", x=386.281506, y=-136.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.kawasaki.ninja", x=386.281506, y=-133.417725)
    # spawn_crossbike(world, blueprint_library, g_vehicle_list, "vehicle.kawasaki.ninja", x=386.281506, y=-130.417725)

    """ego前方卡车布置"""
    car_A = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]
    car_A_transform = carla.Transform(carla.Location(x=388.381506, y=-139.445007, z=0.281942),carla.Rotation(pitch=0.000000, yaw=90.439095, roll=0.000000))
    vehicle_car_A = world.spawn_actor(car_A, car_A_transform)
    g_vehicle_list.append(vehicle_car_A)

    """ego布置"""
    vehicle_bp_hgv = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]
    # vehicle_hgv = world.spawn_actor(vehicle_bp_hgv, spawn_points[28])
    car_C_transform = carla.Transform(carla.Location(x=388.482, y=-154.745, z=0.281942),
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
    display_manager = DisplayManager(grid_size=[2, 3], window_size=[carla_config.DisplayWindows['W'],carla_config.DisplayWindows['H']])
    display_rgb_pos =    {0: [0, 1], 1: [0, 0], 2:[0, 2],
                          3: [1, 0], 4: [1, 2], 5:[1, 1]}
    display_lidar_pos =  {0: [0, 4], 1: [0, 3], 2:[0, 5],
                          3: [1, 3], 4: [1, 5], 5:[1, 4]}
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
        print("aaaa",carla_config.SensorLiDAR_set)
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




    # for i, vehicle in enumerate(g_vehicle_list):
    #     vehicle.set_autopilot(carla_config.World["set_vehicle_list_autopilot"], TM.get_port())



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


