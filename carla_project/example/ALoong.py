
import glob
import os
import sys
import carla
from carla_project.carla_simu.argparser import parse_arguments
from carla_project.carla_simu.run_simulation import run_simulation
from shapely.affinity import rotate

try:
    sys.path.append(glob.glob('/home/didi/carla_project/PythonAPI/carla_project/dist/carla_project-*%d.%d-%s.egg' % (
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

def parse_args():
    argparser = argparse.ArgumentParser(description='CARLA tutorial')

    argparser.add_argument('--host', metavar='H', default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument('-p', '--port', metavar='P', default=2000, type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument('--tm_port', default=8000, type=int,
         help='Traffic Manager Port (default: 8000)')
    argparser.add_argument('--sync', default=False, action='store_true',
          help='Synchronous mode execution')


from carla_project.example.dynamic_weather import set_custom_weather


def spawn_vehicles(world, blueprint_library, spawn_points, vehicle_types, spawn_indices, vehicle_list):
    try:
        for i, index in enumerate(spawn_indices):
            vehicle_bp = blueprint_library.filter(vehicle_types[i % len(vehicle_types)])[0]
            vehicle = world.spawn_actor(vehicle_bp, spawn_points[index])
            vehicle_list.append(vehicle)
    except Exception as e:
        print(f"Error spawning vehicle: {e}")
    return vehicle_list


def main_run_carla(args, client, world, TM,vehicle_list):


    # 设置观察者视角
    spectator = world.get_spectator()
    spectator.set_transform(carla.Transform(carla.Location(x=390., y=-200., z=50), carla.Rotation(pitch=-30,yaw=90,)))


    # 获取spawn点
    spawn_points = world.get_map().get_spawn_points()
    # 在地图上用数字标出刷出点的位置
    for i, spawn_point in enumerate(spawn_points):
        world.debug.draw_string(spawn_point.location, str(i), life_time=10000000)


    # 实例化其他车辆
    spawn_indices = [20,18,21,66,64,67,17,15,284,282,285,286,236,234,237,28]
    vehicle_types = [
        'vehicle.tesla.model3', 'vehicle.tesla.model3', 'vehicle.tesla.model3',
        'vehicle.tesla.model3', 'vehicle.tesla.model3'
    ]
    blueprint_library = world.get_blueprint_library()
    vehicle_list = spawn_vehicles(world, blueprint_library, spawn_points, vehicle_types, spawn_indices, vehicle_list)



    # 卡车自动驾驶
    vehicle_bp_hgv = blueprint_library.filter('vehicle.carlamotors.european_hgv')[0]
    vehicle_hgv = world.spawn_actor(vehicle_bp_hgv, spawn_points[19])
    vehicle_hgv.set_autopilot(True, TM.get_port())
    vehicle_list.append(vehicle_hgv)


    for v in vehicle_list:
        TM.auto_lane_change(v, True)
        v.set_autopilot(True, TM.get_port())









    # 选择路径
    route_1_indices = [65, 16, 283, 26, 31, 317, 371]
    route_1 = [spawn_points[ind].location for ind in route_1_indices]



    # 在同步模式，我们需要设置俯视图的观察者视角

    while True:
        world.tick()




if __name__ == '__main__':


    vehicle_list = []
    args = parse_arguments()
    client = carla.Client(args.host, args.port)
    client.set_timeout(5.0)
    world = client.load_world('Town04')
    set_custom_weather(world)
    original_settings = world.get_settings()
    # 获取场景中的蓝图
    blueprint_library = world.get_blueprint_library()

    # TM 设计为在同步模式下工作
    TM = client.get_trafficmanager(args.tm_port)
    TM.set_synchronous_mode(True)
    TM.global_percentage_speed_difference(80.0)


    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    settings.actor_active_distance = 2000
    world.apply_settings(settings)  # 距离主车距离超过2km的车辆将睡眠。
    try:

        main_run_carla(args,client,world,TM,vehicle_list)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    finally:
        settings.synchronous_mode = False
        TM.set_synchronous_mode(False)
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicle_list])


