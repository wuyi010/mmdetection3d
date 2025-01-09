import json
import carla

def get_config_positions_from_json(file_path, display=False):
    """
    从指定的 JSON 文件路径读取 RGB 配置，转换为字典对象列表。

    参数:
        file_path (str): JSON 文件的路径。
        display (bool): 是否打印读取的对象。
    """
    # 从 JSON 文件中读取
    with open(file_path, 'r') as f:
        transform_data = json.load(f)
    # 验证读取结果
    if display:
        for item in transform_data:
            print(item)
    print("读取RGB 配置：")
    return transform_data

def get_config_file_to_transform(file_path, display=False):
    """
        从指定的 JSON 文件路径读取 RGB 配置，转换为 carla_project.Transform 对象列表。

        参数:
            file_path (str): JSON 文件的路径。
            display (bool): 是否打印读取的 carla_project.Transform 对象。
    """

    # 从 JSON 文件中读取
    with open(file_path, 'r') as f:
        transform_data = json.load(f)

    # 转换为 carla_project.Transform 对象
    transform_positions = [
        carla.Transform(
            carla.Location(item['location']['x'], item['location']['y'], item['location']['z']),
            carla.Rotation(item['rotation']['pitch'], item['rotation']['yaw'], item['rotation']['roll'])
        ) for item in transform_data
    ]

    # 验证读取结果
    if display:
        for transform in transform_positions:
            print(transform)
    print("读取完毕：",transform_positions)
    return transform_positions


def get_config_sensor_options(file_path):
    """
    file_path = config_sensor_options_lidar
    file_path = config_sensor_options_RGBCamera
    Args:
        file_path:

    Returns:

    """
 # 从 JSON 文件读取并加载到字典
    with open(file_path, 'r') as json_file:
        sensor_options = json.load(json_file)
    # 查看加载后的字典
    print(sensor_options)
    return sensor_options