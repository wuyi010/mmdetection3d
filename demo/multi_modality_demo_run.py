# Copyright (c) OpenMMLab. All rights reserved.
import logging
import os
from argparse import ArgumentParser

from mmengine.logging import print_log

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




if __name__ == '__main__':
    main_run()
