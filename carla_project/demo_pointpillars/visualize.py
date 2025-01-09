from carla_project.carla_tool.B_fun_visualizer import is_same_object
from carla_project.carla_tool.draw_bboxes_3d import draw_bboxes_3d
from carla_project import config

import os
import json
import numpy as np

from config import carla_config


def carla_dataset_vis(base_dir, bin_file_path, output_dir):

    # 定义目录和范围

    camera_dirs = dataset_list_name_list[:5]
    preds_subdir = "preds"

    folder_path = os.path.join(base_dir, bin_file_path)
    print("folder_path:", folder_path)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    print("file_count", file_count)
    file_range = range(file_count)  # 对应从000000到000030

    # 遍历每个目录和文件
    ego = [0, 0, -2, 7, 2.6, 3.46, 0]
    point_center = [0, 0, -2, 0.05, 0.05, 0.05, 0]
    folder_path_outputs = os.path.join(base_dir, output_dir)

    position_threshold = 0.6  # 位置差异的阈值
    size_threshold = 0.4  # 尺寸差异的阈值
    point_listdir = os.listdir(folder_path)
    print(point_listdir)

    # 使用列表推导式过滤掉包含 '-col' 的文件名
    filtered_list = [file for file in point_listdir if file.endswith('.bin') and '-col' not in file]
    print(filtered_list)

    # 遍历所有的bin文件
    for bin_file in filtered_list:
        bin_name = bin_file.split('.')[0]
        all_labels = []
        all_scores = []
        all_bboxes = []

        # 定义预测结果文件路径
        file_paths = []
        for dirname in carla_config.SensorCameraName:
            file_path = os.path.join(folder_path_outputs, dirname, preds_subdir, f"{bin_name}.json")
            file_paths.append(file_path)

        # 读取每个json文件并提取标签、得分和3D框
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                data = json.load(f)
                all_labels.extend(data['labels_3d'])
                all_scores.extend(data['scores_3d'])
                all_bboxes.extend(data['bboxes_3d'])

        # 将数据转为 numpy 数组
        all_labels = np.array(all_labels)
        all_scores = np.array(all_scores)
        all_bboxes = np.array(all_bboxes)

        # 最终保留的框、得分和标签
        final_bboxes = []
        final_scores = []
        final_labels = []

        # 逐个检查不同摄像头的预测框
        num_bboxes = len(all_bboxes)
        for index in range(num_bboxes):
            is_duplicate = False
            current_bbox = all_bboxes[index]
            current_score = all_scores[index]
            current_label = all_labels[index]

            # 和已保留的框进行比较，判断是否是重复的框
            for j in range(len(final_bboxes)):
                existing_bbox = final_bboxes[j]
                existing_score = final_scores[j]

                # 比较框的位置和大小是否相似
                if is_same_object(current_bbox, existing_bbox, position_threshold, size_threshold):
                    # 如果位置和尺寸差异在阈值内，认为是重复的框
                    is_duplicate = True
                    # 如果当前框的得分更高，替换已有的框
                    if current_score > existing_score:
                        final_bboxes[j] = current_bbox
                        final_scores[j] = current_score
                        final_labels[j] = current_label
                    break  # 已经找到重复的框，退出内层循环

            if not is_duplicate:
                # 如果没有找到重复的框，将当前框添加到结果中
                final_bboxes.append(current_bbox)
                final_scores.append(current_score)
                final_labels.append(current_label)

        # 最终的合并结果是 final_bboxes, final_scores, final_labels
        final_bboxes.append(ego)  # 加入ego框
        final_bboxes.append(point_center)  # 加入point_center框

        # 读取bin文件，绘制框
        bin_dir_sim = os.path.join(folder_path, bin_file)
        print(f"当前图像: {bin_file}")

        # 加载LiDAR点云数据 (假设每个.bin文件包含一个浮点数组，表示点云数据)
        point_cloud_data = np.fromfile(bin_dir_sim, dtype=np.float32).reshape(-1, 4)  # 假设数据是(x, y, z, intensity)

        # 绘制3D框
        draw_bboxes_3d(final_bboxes, point_cloud_data)

if __name__ == '__main__':
    # 基础路径
    base_path = "/home/didi/mmdetection3d_ing/carla_project"

    dataset_path     = os.path.join(base_path, carla_config.CarlaDataPath['dataset_path'])
    lidar_path       = os.path.join(base_path, carla_config.CarlaDataPath['lidar_path'])
    camera_path      = os.path.join(base_path, carla_config.CarlaDataPath['camera_path'])
    mvxnet_pkl_merge = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_pkl_merge'])

    mvxnet_bin_folder =os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_bin_folder'])
    mvxnet_pkl_file   =os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_pkl_file'])
    mvxnet_cal_folder =os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_cal_folder'])
    mvxnet_out_folder =os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_out_folder'])
    mvxnet_path_name =os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_path_name'])



    carla_project_path = "/home/didi/mmdetection3d_ing/carla_project/"
    # carla_dataset_vis(carla_project_path, mvxnet_bin_folder, output_dir)


    # 读取JSON文件
    json_file_path = '/home/didi/mmdetection3d_ing/carla_project/demo_pointpillars/outputs/preds/0000008661.json'
    bin_file_path = "/home/didi/mmdetection3d_ing/carla_project/CarlaData/mvxnet/LidarBin/0000008661.bin"
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    # 提取 bboxes_3d 数据
    bboxes_3d = data.get('bboxes_3d', [])

    draw_bboxes_3d(bboxes_3d,bin_file_path )