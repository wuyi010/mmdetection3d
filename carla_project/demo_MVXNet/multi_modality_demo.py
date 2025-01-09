# Copyright (c) OpenMMLab. All rights reserved.
import logging
import os
import time
from argparse import ArgumentParser

from mmengine.logging import print_log
from tqdm import tqdm

from carla_tool import load_from_pickle
from config import carla_config
from config.carla_config import SensorCameraName
from demo_MVXNet.MVXNet_DatasetCreate import create_dataset_paths_dirs, main_data_mvxnet
from mmdet3d.apis import MultiModalityDet3DInferencer



def main_run():
    """
    demo/multi_modality_demo.py demo/data/kitti/000008.bin demo/data/kitti/000008.png demo/data/kitti/000008.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2 --out-dir ./outputs
    """
    """
    python demo/multi_modality_demo.py demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin demo/data/nuscenes/ demo/data/nuscenes/n015-2018-07-24-11-22-45+0800.pkl projects/BEVFusion/configs/bevfusion_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d.py ${CHECKPOINT_FILE} --cam-type all --score-thr 0.2 --show
    """

    init_args = {'model': '/home/didi/mmdetection3d/configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py',
                'weights': '/home/didi/mmdetection3d/checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth',
                 'device': 'cuda:0'}

    call_args = {'pred_score_thr': 0.3,
                 'out_dir': './outputs',
                 'show': True,
                 'wait_time': -1,
                 'no_save_vis': False,
                 'no_save_pred': False,
                 'print_result': False,
                 'inputs': {'points': 'demo/data/kitti/000008.bin',
                               'img': 'demo/data/kitti/000008.png',
                           'infos': 'demo/data/kitti/000008.pkl'}}



    # TODO: Support inference of point cloud numpy file.
    inferencer = MultiModalityDet3DInferencer(**init_args)
    inferencer(**call_args)




def MVXNetInference(BasePath,carla_project_path,DATASET_path, mvxnet_cal_folder,mvxnet_out_folder,):

    DATASET = load_from_pickle(DATASET_path)


    calibs_path = mvxnet_cal_folder
    create_dataset_paths_dirs([mvxnet_out_folder])

    model_PATH = os.path.join(BasePath,'configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py')
    weights_PATH = os.path.join(BasePath,'checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth')
    # 固定推理参数（这些不会改变）
    init_args = {
        'model': model_PATH,
        'weights': weights_PATH,
        'device': 'cuda:0'}


    inferencer = MultiModalityDet3DInferencer(**init_args)

    call_args_base = {'pred_score_thr': 0.01,
                      'out_dir': mvxnet_out_folder,
                      # 'show': False,  # 关闭显示
                      'show': True,  # 关闭显示
                      'wait_time': -1,
                      'no_save_vis': False,
                      'no_save_pred': False,
                      'print_result': False}

    # 迭代 DATASET 中的每个 timestamp 和数据
    for timestamp, data in tqdm(DATASET.items(), desc="Processing timestamps", total=len(DATASET)):

        # 获取点云路径
        points_path = os.path.join(carla_project_path, data['point']['path'])
        # points_path = "/home/didi/mmdetection3d_ing/carla_project/CarlaData/mvxnet/LidarBin/0000000050.bin"
        # 迭代每个 SensorCameraName
        for name in SensorCameraName:
            call_args = call_args_base.copy()
            img_path = os.path.join(carla_project_path, DATASET[timestamp]['camera'][name]['path'])
            # 获取文件名（不包含扩展名）
            filename_with_extension = os.path.basename(img_path)
            filename, _ = os.path.splitext(filename_with_extension)
            # 获取 infos 路径

            infos_path = os.path.join(carla_project_path, calibs_path, f'{filename}.pkl')
            # 更新 call_args 输入
            # 设置预测结果的输出路径，并根据相机名来命名预测文件
            call_args['out_dir'] = os.path.join(mvxnet_out_folder, f'{name}')
            call_args['inputs'] = {'points': points_path, 'img': img_path, 'infos': infos_path, 'cam-type': "CAM2"}
            # 调用推理函数
            inferencer(**call_args)
            # 暂停 0.1 秒，模拟处理时间
            time.sleep(0.01)

if __name__ == '__main__':
    # main_run()

    main_data_mvxnet()


    base_path = "/home/didi/mmdetection3d_ing/carla_project"

    dataset_path = os.path.join(base_path, carla_config.CarlaDataPath['dataset_path'])
    lidar_path = os.path.join(base_path, carla_config.CarlaDataPath['lidar_path'])
    camera_path = os.path.join(base_path, carla_config.CarlaDataPath['camera_path'])

    mvxnet_bin_folder = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_bin_folder'])
    mvxnet_pkl_file = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_pkl_file'])
    mvxnet_cal_folder = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_cal_folder'])
    mvxnet_out_folder = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_out_folder'])
    mvxnet_path_name = os.path.join(base_path, carla_config.CarlaDataPath['mvxnet_path_name'])

    BasePath =f"/home/didi/mmdetection3d_ing"
    """一. 推理"""
    DATASET_path = mvxnet_pkl_file
    carla_project_path =base_path
    MVXNetInference(BasePath, carla_project_path, DATASET_path, mvxnet_cal_folder, mvxnet_out_folder, )