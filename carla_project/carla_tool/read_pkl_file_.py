

"""读取pkl"""
import pickle


def load_kitti_pickle(file_path):
    """读取 KITTI 数据集的 .pkl 文件"""
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data

def read_pkl_file(file_path):
    """
    Args:
        file_path: .pkl 文件路径
    Returns:

    """
    kitti_data = load_kitti_pickle(file_path)

    # 打印读取到的数据
    print("读取的 KITTI 数据：", kitti_data)

    # 如果需要，可以访问特定的字段，比如 images
    # images = kitti_data.get('data_list', [])[0].get('images', {}).get('CAM2',{})
    # lidar = kitti_data.get('data_list', [])[0].get('lidar_points', {})
    # print("images信息：", images)
    # print("lidar信息：", lidar)


if __name__ == '__main__':

    read_pkl_file("/home/didi/mmdetection3d/demo/data/kitti/000008.pkl")

    read_pkl_file("/home/didi/mmdetection3d/demo/data/nuscenes/n015-2018-07-24-11-22-45+0800.pkl")
