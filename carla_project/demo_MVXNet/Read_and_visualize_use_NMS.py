from carla_project.carla_tool.B_fun_visualizer import is_same_object
from carla_project.carla_tool.draw_bboxes_3d import draw_bboxes_3d
from carla_project import config

import os
import json

from config import carla_config


def carla_dataset_vis(base_dir,bin_file_path,output_dir):


    # 定义目录和范围
    preds_subdir = "preds"

    folder_path = os.path.join(base_dir, bin_file_path)
    print("folder_path:",folder_path)
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    print("folder_path:",folder_path)
    print("file_count",file_count)
    file_range = range(file_count)  # 对应从000000到000030



    # 遍历每个目录和文件
    # Vehicledimensions = Length = 7.94, Width = 2.89, Height = 3.46
    ego = [0, 0, -2, 7, 2.6, 3.46, 0]
    ego = [0, 0, -2, 7, 2.6, 4, 0]
    point_center = [0, 0, -2, 0.05, 0.05, 0.05, 0]
    folder_path_outputs = os.path.join(base_dir, output_dir)

    position_threshold = 0.5  # 位置差异的阈值    # 定义阈值，用于判断两个框是否是重复的 (可以调整这个阈值)
    size_threshold = 0.5  # 尺寸差异的阈值
    point_listdir = os.listdir(folder_path)
    print(point_listdir)
    # 使用列表推导式过滤掉包含 '-col' 的文件名
    filtered_list = [file for file in point_listdir if file.endswith('.bin') and '-col' not in file]
    print(filtered_list)

    for bin_file in filtered_list:
        bin_name = bin_file.split('.')[0]
        # i= input_which_one
        all_labels = []
        all_scores = []
        all_bboxes = []

        # 定义预测结果文件路径
        file_paths = []
        for dirname in carla_config.SensorCameraName:
            file_path = os.path.join(folder_path_outputs, dirname, preds_subdir, f"{bin_name}.json")
            file_paths.append(file_path)
        # print(file_paths)

        for file_path in file_paths:
            with open(file_path, 'r') as f:
                data = json.load(f)
                all_labels.extend(data['labels_3d'])
                all_scores.extend(data['scores_3d'])
                all_bboxes.extend(data['bboxes_3d'])
            # 将数据转为 numpy 数组
        import numpy as np
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
                if is_same_object(current_bbox, existing_bbox,position_threshold,size_threshold):
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

        # print(f"最终保留的得分: {final_scores}")
        # print(f"最终保留的框: {final_bboxes}")
        final_bboxes.append(ego)
        final_bboxes.append(point_center)
        bin_dir_sim = os.path.join(folder_path,  bin_file)
        print(f"当前图像:",  bin_file)
        draw_bboxes_3d(final_bboxes, bin_dir_sim)




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
    carla_dataset_vis(base_dir=carla_project_path, bin_file_path=mvxnet_bin_folder, output_dir=mvxnet_out_folder)