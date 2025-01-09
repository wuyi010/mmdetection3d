# Copyright (c) OpenMMLab. All rights reserved.
import os
from argparse import ArgumentParser

import mmcv

from mmdet3d.apis import inference_multi_modality_detector, init_model
from mmdet3d.registry import VISUALIZERS


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('pcd', help='Point cloud file')
    parser.add_argument('img', help='image file')
    parser.add_argument('ann', help='ann file')
    # parser.add_argument('Sensor_cfg', help='Config file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--cam-type',
        type=str,
        default='CAM_FRONT',
        help='choose camera type to inference')
    parser.add_argument(
        '--score-thr', type=float, default=0.0, help='bbox score threshold')
    parser.add_argument(
        '--out-dir', type=str, default='demo', help='dir to save results')
    parser.add_argument(
        '--show',
        action='store_true',
        help='show online visualization results')
    parser.add_argument(
        '--snapshot',
        action='store_true',
        help='whether to save online visualization results')
    args = parser.parse_args()
    return args


def main(args):
    # build the model from a Sensor_cfg file and a checkpoint file
    model = init_model(args.config, args.checkpoint, device=args.device)
    # print("bevfusion model\n",model)

    # init visualizer
    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta

    # test a single image and point cloud sample
    result, data = inference_multi_modality_detector(model, args.pcd, args.img,
                                                     args.ann, args.cam_type)
    points = data['inputs']['points']
    if isinstance(result.img_path, list):
        img = []
        for img_path in result.img_path:
            single_img = mmcv.imread(img_path)
            single_img = mmcv.imconvert(single_img, 'bgr', 'rgb')
            img.append(single_img)
    else:
        img = mmcv.imread(result.img_path)
        img = mmcv.imconvert(img, 'bgr', 'rgb')
    data_input = dict(points=points, img=img)

    # print(data)
    # print(result)
    # show the results
    visualizer.add_datasample(
        'result',
        data_input,
        data_sample=result,
        draw_gt=False,
        show=args.show,
        wait_time=-1,
        out_file=args.out_dir,
        pred_score_thr=args.score_thr,
        vis_task='multi-modality_det')




from types import SimpleNamespace
def carla_bevfusion_show():
    name =f"0000020355"
    args = SimpleNamespace(
            # ann='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/0000020355.pkl',
            ann=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/{name}.pkl',
            cam_type='all',
            checkpoint='/home/didi/mmdetection3d_ing/checkpoints/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-fixed.pth',
            config='/home/didi/mmdetection3d_ing/projects/BEVFusion/configs/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d.py',
            device='cuda:0',
            img='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Camera',
            out_dir='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/output',
            pcd=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/LidarBin/{name}.bin',
            score_thr=0.1,
            show=True,
            # show=False,
            snapshot=True
        )
    # build the model from a Sensor_cfg file and a checkpoint file
    model = init_model(args.config, args.checkpoint, device=args.device)
    # print("bevfusion model\n",model)

    # init visualizer
    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta

    # 目录路径
    folder_path = '/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/LidarBin'
    # 遍历目录中的文件
    for filename in os.listdir(folder_path):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        # 仅处理文件（跳过目录）
        if os.path.isfile(file_path):
            # 获取文件名去除扩展名
            name, extension = os.path.splitext(filename)

            print(f"File name without extension: {name}")
            # name = f"0000012182"
            args2 = SimpleNamespace(
                ann=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/{name}.pkl',
                pcd=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/LidarBin/{name}.bin',
            )
            # test a single image and point cloud sample
            result, data = inference_multi_modality_detector(model, args2.pcd, args.img,
                                                             args2.ann, args.cam_type)
            points = data['inputs']['points']
            if isinstance(result.img_path, list):
                img = []
                for img_path in result.img_path:
                    single_img = mmcv.imread(img_path)
                    single_img = mmcv.imconvert(single_img, 'bgr', 'rgb')
                    img.append(single_img)
            else:
                img = mmcv.imread(result.img_path)
                img = mmcv.imconvert(img, 'bgr', 'rgb')
            data_input = dict(points=points, img=img)

            # print(data)
            # print(result)
            # show the results
            visualizer.add_datasample(
                'result',
                data_input,
                data_sample=result,
                draw_gt=False,
                show=args.show,
                wait_time=-1,
                out_file=args.out_dir,
                pred_score_thr=args.score_thr,
                vis_task='multi-modality_det')

def carla_bevfusion():
    name =f"0000020355"
    args = SimpleNamespace(
            # ann='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/0000020355.pkl',
            ann=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/{name}.pkl',
            cam_type='all',
            checkpoint='/home/didi/mmdetection3d_ing/checkpoints/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-fixed.pth',
            config='/home/didi/mmdetection3d_ing/projects/BEVFusion/configs/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d.py',
            device='cuda:0',
            img='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Camera',
            out_dir='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/output',
            pcd=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/LidarBin/{name}.bin',
            score_thr=0.1,
            # show=True,
            show=False,
            snapshot=True
        )
    # build the model from a Sensor_cfg file and a checkpoint file
    model = init_model(args.config, args.checkpoint, device=args.device)
    # print("bevfusion model\n",model)

    # init visualizer
    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta

    # 目录路径
    folder_path = '/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/LidarBin'
    # 遍历目录中的文件
    for filename in os.listdir(folder_path):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        # 仅处理文件（跳过目录）
        if os.path.isfile(file_path):
            # 获取文件名去除扩展名
            name, extension = os.path.splitext(filename)

            print(f"File name without extension: {name}")
            # name = f"0000012182"
            args2 = SimpleNamespace(
                ann=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/{name}.pkl',
                pcd=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/LidarBin/{name}.bin',
            )
            # test a single image and point cloud sample
            result, data = inference_multi_modality_detector(model, args2.pcd, args.img,
                                                             args2.ann, args.cam_type)
            points = data['inputs']['points']
            if isinstance(result.img_path, list):
                img = []
                for img_path in result.img_path:
                    single_img = mmcv.imread(img_path)
                    single_img = mmcv.imconvert(single_img, 'bgr', 'rgb')
                    img.append(single_img)
            else:
                img = mmcv.imread(result.img_path)
                img = mmcv.imconvert(img, 'bgr', 'rgb')
            data_input = dict(points=points, img=img)

            # print(data)
            # print(result)
            # show the results
            visualizer.add_datasample(
                'result',
                data_input,
                data_sample=result,
                draw_gt=False,
                show=args.show,
                wait_time=-1,
                out_file=args.out_dir,
                pred_score_thr=args.score_thr,
                vis_task='multi-modality_det')


if __name__ == '__main__':
    # args = parse_args()
    # 模拟命令行参数
    carla_bevfusion()
    # # 目录路径
    # name = f'0000020355'
    # args = SimpleNamespace(
    #     # ann='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/0000020355.pkl',
    #     ann=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Calibs/{name}.pkl',
    #     cam_type='all',
    #     checkpoint='/home/didi/mmdetection3d_ing/checkpoints/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-fixed.pth',
    #     config='/home/didi/mmdetection3d_ing/projects/BEVFusion/configs/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d.py',
    #     device='cuda:0',
    #     img='/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/Camera',
    #     out_dir='/carla_project/config/bevfusion/output',
    #     pcd=f'/home/didi/mmdetection3d_ing/carla_project/CarlaData/bevfusion/LidarBin/{name}.bin',
    #     score_thr=0.1,
    #     show=True,
    #     # show=False,
    #     snapshot=True
    # )
    # # 直接调用 main(args)
    # main(args)


"""
_________________
python projects/BEVFusion/demo/multi_modality_demo.py demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin demo/data/nuscenes/ demo/data/nuscenes/n015-2018-07-24-11-22-45+0800.pkl projects/BEVFusion/configs/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d.py /home/didi/mmdetection3d_ing_ing/checkpoints/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-fixed.pth --cam-type all --score-thr 0.2 --show --snapshot
-----------------

            multi_modality_demo.py 
pcd         n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin 
img         demo/data/nuscenes/ 
ann         n015-2018-07-24-11-22-45+0800.pkl 
config      bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d.py 
checkpoint  bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-fixed.pth 
--cam-type  all 
--score-thr 0.2 
--show
"""
