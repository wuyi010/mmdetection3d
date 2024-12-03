# Copyright (c) OpenMMLab. All rights reserved.
import logging
from argparse import ArgumentParser

from mmengine.logging import print_log

from mmdet3d.apis import LidarDet3DInferencer


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('pcd', help='Point cloud file')
    parser.add_argument('model', help='Config file')
    parser.add_argument('weights', help='Checkpoint file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--pred-score-thr',
        type=float,
        default=0.3,
        help='bbox score threshold')
    parser.add_argument(
        '--out-dir',
        type=str,
        default='outputs',
        help='Output directory of prediction and visualization results.')
    parser.add_argument(
        '--show',
        action='store_true',
        help='Show online visualization results')
    parser.add_argument(
        '--wait-time',
        type=float,
        default=-1,
        help='The interval of show (s). Demo will be blocked in showing'
        'results, if wait_time is -1. Defaults to -1.')
    parser.add_argument(
        '--no-save-vis',
        action='store_true',
        help='Do not save detection visualization results')
    parser.add_argument(
        '--no-save-pred',
        action='store_true',
        help='Do not save detection prediction results')
    parser.add_argument(
        '--print-result',
        action='store_true',
        help='Whether to print the results.')
    call_args = vars(parser.parse_args())

    call_args['inputs'] = dict(points=call_args.pop('pcd'))

    if call_args['no_save_vis'] and call_args['no_save_pred']:
        call_args['out_dir'] = ''

    init_kws = ['model', 'weights', 'device']
    init_args = {}
    for init_kw in init_kws:
        init_args[init_kw] = call_args.pop(init_kw)

    # NOTE: If your operating environment does not have a display device,
    # (e.g. a remote server), you can save the predictions and visualize
    # them in local devices.
    if os.environ.get('DISPLAY') is None and call_args['show']:
        print_log(
            'Display device not found. `--show` is forced to False',
            logger='current',
            level=logging.WARNING)
        call_args['show'] = False

    return init_args, call_args


def main():
    # TODO: Support inference of point cloud numpy file.
    # init_args, call_args = parse_args()
    #
    # print('init_args :',init_args)
    # print('call_args :',call_args)


    init_args  = {
        'model': '/home/didi/mmdetection3d/configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py',
        # 'model': '/home/didi/mmdetection3d/configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py',
        'weights': '/home/didi/mmdetection3d/checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth',
                  'device': 'cuda:0'}

    i = 0
    file_name = f'{i:06d}'
    call_args  = {'pred_score_thr': 0.01,
                  'out_dir': 'outputs',
                  'show': True,
                  # 'show': False,
                  'wait_time': -1,
                  'no_save_vis': False,
                  'no_save_pred': False,
                  'print_result': False,
                  # 'inputs': {'points': '/home/didi/mmdetection3d/data/kitti/testing/velodyne/000000.bin'}}
                  # 'inputs': {'points': '/home/didi/mmdetection3d/data/kitti/testing/RainySimSet_velodyne_reduced/000030.bin'}}
                  # 'inputs': {'points': f'/home/didi/mmdetection3d/carla_project/Carla_data_map3_plan2_vehicle/dataset/points/000000.bin'}}
                  'inputs': {'points': f'/home/didi/mmdetection3d/carla_project/Carla_data_map4_plan1_vehicle/dataset/points/000000.bin'}}


    inferencer = LidarDet3DInferencer(**init_args)
    inferencer(**call_args)

    if call_args['out_dir'] != '' and not (call_args['no_save_vis']  and call_args['no_save_pred']):
        print_log(f'results have been saved at {call_args["out_dir"]}',logger='current')


import os


def main_full(name):
    # 初始化推理器（放在循环外部，只初始化一次）
    init_args = {
        # 'model': '/home/didi/mmdetection3d/configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py',
        'model': '/home/didi/mmdetection3d/configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py',
        'weights': '/home/didi/mmdetection3d/checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth',
        'device': 'cuda:0'}

    inferencer = LidarDet3DInferencer(**init_args)

    # 固定推理参数（这些不会改变）
    call_args_base = {'pred_score_thr': 0.01,
                      'out_dir': 'outputs',
                      'show': True,  # 关闭显示
                      'wait_time': -1,
                      'no_save_vis': False,
                      'no_save_pred': False,
                      'print_result': False}

    i = name
    # 循环从 000000 到 000030
    # for i in range(31):  # 生成从 000000 到 000030 的文件名
    # 生成文件名（六位数，前面补零）
    file_name = f'{i:06d}.bin'
    file_path = os.path.join('/data/kitti/testing/velodyne', file_name)

    # 更新输入路径
    call_args = call_args_base.copy()
    call_args['inputs'] = {'points': file_path}

    # 打印当前文件名
    print(f'Processing file: {file_path}')

    # 执行推理
    # 执行推理并打印结果
    result = inferencer(**call_args)
    # 输出推理结果
    print(f'Results for {file_name}: {result}')

    # 保存结果
    if call_args['out_dir'] != '' and not (call_args['no_save_vis']
                                           and call_args['no_save_pred']):
        print_log(
            f'results have been saved at {call_args["out_dir"]}',
            logger='current')



if __name__ == '__main__':
    main()
    # main_full(0)



    """
python data/kitti/testing/velodyne/000001.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth --show
python demo/pcd_demo.py demo/data/kitti/000008.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth --show

    """

    """
    python demo/pcd_demo.py data/custom/dataset/point_L5/000000.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  



    python demo/pcd_demo.py data/custom/dataset/point_L5/000004.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  

    """

    """
python demo/pcd_demo.py data/custom/dataset/point_L5/000000.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  --show
python demo/pcd_demo.py data/custom/dataset/point_L5/000001.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  --show
python demo/pcd_demo.py data/custom/dataset/point_L5/000002.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  --show
python demo/pcd_demo.py data/custom/dataset/point_L5/000003.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  --show
python demo/pcd_demo.py data/custom/dataset/point_L5/000004.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  --show

    """