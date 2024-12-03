# Copyright (c) OpenMMLab. All rights reserved.
import logging
import os
import pickle
import time
from argparse import ArgumentParser

from mmengine.logging import print_log
from pygame.time import delay

from mmdet3d.apis import MultiModalityDet3DInferencer

def carla_inference():
    init_args = {
        'model': '/home/didi/mmdetection3d/configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py',
        'weights': '/home/didi/mmdetection3d/checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth',
        'device': 'cuda:0'}
    # 固定推理参数（这些不会改变）
    call_args_base = {'pred_score_thr': 0.01,
                      'out_dir': '/home/didi/mmdetection3d/carla_project/Carla_data/outputs/',
                      # 'show': True,  # 关闭显示
                      'show': False,  # 关闭显示
                      'wait_time': -1,
                      'no_save_vis': False,
                      'no_save_pred': False,
                      'print_result': False}

    # TODO: Support inference of point cloud numpy file.
    inferencer = MultiModalityDet3DInferencer(**init_args)
    folder_path = '/home/didi/mmdetection3d/carla_project/Carla_data/dataset/points'

    # 获取文件数量
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    from carla_project.A0_config import dataset_list_name_list

    list_cam = dataset_list_name_list[:5]
    for dataset_name in list_cam:
        cam_name = dataset_name
        # 复制 call_args_base
        call_args = call_args_base.copy()

        # 更新 out_dir，将 dataset_name 作为输出目录的一部分
        call_args['out_dir'] = f'/home/didi/mmdetection3d/carla_project/Carla_data/outputs/{dataset_name}'
        """ 'CAM_FRONT_LEFT',  'CAM_BACK_LEFT', 'CAM_FRONT_RIGHT',   'CAM_BACK_RIGHT',   'CAM_FRONT', """

        # for i in range(file_count):
        from tqdm import tqdm  # 导入 tqdm 库
        for i in tqdm(range(file_count), desc=f"Processing files for {cam_name}"):
            # 更新输入路径

            index = f'{i:06d}'
            points_path = os.path.join('/home/didi/mmdetection3d/carla_project/Carla_data/dataset/points',
                                       f'{index}.bin')
            img_path = os.path.join(f'/home/didi/mmdetection3d/carla_project/Carla_data/dataset/{cam_name}',
                                    f'{index}.png')
            infos_path = os.path.join(f'/home/didi/mmdetection3d/carla_project/Carla_data/dataset/pkl/{cam_name}',
                                      f'{index}.pkl')
            call_args['inputs'] = {'points': points_path, 'img': img_path, 'infos': infos_path, 'cam-type ': "CAM2", }
            inferencer(**call_args)
            time.sleep(0.1)

from carla_project.carla_tool.B_fun_visualizer import visualize_bboxes_3d_carla
if __name__ == '__main__':
    carla_inference()
    # visualize_bboxes_3d_carla()