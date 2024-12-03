import numpy as np


def read_bin_file(bin_file_path):
    """
    读取KITTI格式的.bin文件并返回点云数据。
    参数: bin_file_path (str): .bin文件的路径。
    返回:  np.ndarray: 包含点云的numpy数组，格式为 (N, 4)，其中N为点的数量，4列分别为X, Y, Z, 强度。
    """
    # 读取二进制文件
    point_cloud_data = np.fromfile(bin_file_path, dtype=np.float32)
    # 检查数据是否为4的倍数
    if len(point_cloud_data) % 4 != 0:
        raise ValueError("点云数据的长度不是4的倍数，请检查输入文件。")
    point_cloud_data = point_cloud_data.reshape(-1, 4) # 重新塑形为(N, 4)的数组
    return point_cloud_data