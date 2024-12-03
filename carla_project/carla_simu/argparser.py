import argparse


def parse_arguments():
    argparser = argparse.ArgumentParser(description='CARLA Sensor tutorial')

    argparser.add_argument('--host', metavar='H', default='127.0.0.1',
                           help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument('-p', '--port', metavar='P', default=2000, type=int,
                           help='TCP port to listen to (default: 2000)')
    argparser.add_argument('--tm_port', default=8000, type=int,
                           help='Traffic Manager Port (default: 8000)')
    argparser.add_argument('--sync', default=False, action='store_true',
                           help='Synchronous mode execution')
    argparser.set_defaults(sync=True)

    argparser.add_argument('--res', metavar='WIDTHxHEIGHT', default='9600x2160',
                           help='Window resolution (default: 1920x1080)')
    argparser.add_argument('--IM', metavar='WIDTHxHEIGHT', default='1920x1080',
                           help='Window resolution for image cam (default: 512x512)')

    argparser.add_argument('--save-path', default='Carla_data/',
                           help='Save path for sensor data')
    argparser.add_argument('--lidar_path', default='lidar/',
                           help='Save path for lidar')
    argparser.add_argument('--camera_path', default='camera/',
                           help='Save path for camera')
    argparser.add_argument('--lidar_merge_path', default='lidar_merge/',
                           help='Save path for lidar ply merge')

    args = argparser.parse_args()

    # Extract resolution dimensions
    args.width, args.height = [int(x) for x in args.res.split('x')]
    args.IM_WIDTH, args.IM_HEIGHT = [int(x) for x in args.IM.split('x')]

    return args


# 调用函数并获取解析后的参数
if __name__ == "__main__":
    args = parse_arguments()
    print(args)  # 输出解析后的参数


    """
    
   

    """
