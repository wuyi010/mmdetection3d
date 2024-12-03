import os
from PIL import Image


def get_prefix(file_name):
    return file_name.split('-')[0]


def check_and_clean_images_and_lidar(camera_dir, lidar_dir):
    # 定义函数来获取文件前缀

    # 初始化字典来存储前缀及其对应的文件
    prefix_files = {}
    # 遍历文件夹下所有的文件
    for file_name in os.listdir(camera_dir):
        if file_name.endswith('.png'):
            file_path = os.path.join(camera_dir, file_name)

            # 检查文件是否可以打开
            try:
                with Image.open(file_path) as img:
                    img.verify()  # 验证图像文件是否正常
            except (IOError, SyntaxError):
                # 如果无法打开图片，则删除该文件
                print(f"Cannot open {file_name}, deleting it.")
                os.remove(file_path)
                continue

            # 获取文件前缀
            prefix = get_prefix(file_name)

            # 将文件按前缀存入字典
            if prefix not in prefix_files:
                prefix_files[prefix] = []
            prefix_files[prefix].append(file_name)

    # 遍历字典，检查每个前缀的文件数量
    for prefix, files in prefix_files.items():
        if len(files) != 5:
            # 如果前缀对应的文件数量不是 5，将该前缀的所有文件删除
            print(f"Prefix {prefix} does not have 5 files, deleting all its files.")
            for file_name in files:
                file_path = os.path.join(camera_dir, file_name)
                os.remove(file_path)

    # 重新遍历文件夹，获取所有剩下的文件的前缀列表
    remaining_prefixes = set()
    for file_name in os.listdir(camera_dir):
        if file_name.endswith('.png'):
            remaining_prefixes.add(get_prefix(file_name))
    print("Remaining file prefixes:", remaining_prefixes)

    # 遍历 lidar 文件夹下的所有 .ply 文件
    for file_name in os.listdir(lidar_dir):
        if file_name.endswith('.ply'):
            file_path = os.path.join(lidar_dir, file_name)

            # 获取文件前缀
            prefix = get_prefix(file_name)

            # 检查前缀是否在 remaining_prefixes 中
            if prefix not in remaining_prefixes:
                # 如果前缀不在 remaining_prefixes 中，则删除该文件
                print(f"Prefix {prefix} not found in remaining_prefixes, deleting file: {file_name}")
                os.remove(file_path)




if __name__ == "__main__":
    # 使用的目录
    # 使用的camera目录和lidar目录
    camera_directory = "/home/didi/mmdetection3d/carla_project/Carla_data/camera"
    lidar_directory = "/home/didi/mmdetection3d/carla_project/Carla_data/lidar"
    check_and_clean_images_and_lidar(camera_directory, lidar_directory)

