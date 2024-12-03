


import numpy as np
import time
import torch
import open3d as o3d
from matplotlib import pyplot as plt
import mmcv
import numpy as np
from mmengine import load
from mmdet3d.structures import CameraInstance3DBoxes
from mmdet3d.visualization import Det3DLocalVisualizer
from mmdet3d.structures import LiDARInstance3DBoxes

"""在图像上绘制投影的 3D 框"""
def draw_proj_bboxes_3d(pkl_dir='../data/kitti/000008.pkl',png_dir ='../data/kitti/000008.png' ):
    info_file = load(pkl_dir)
    cam2img = np.array(info_file['data_list'][0]['images']['CAM2']['cam2img'], dtype=np.float32)
    print(cam2img.shape)
    print(cam2img)
    bboxes_3d = []
    for instance in info_file['data_list'][0]['instances']:
        bboxes_3d.append(instance['bbox_3d'])
    gt_bboxes_3d = np.array(bboxes_3d, dtype=np.float32)
    gt_bboxes_3d = CameraInstance3DBoxes(gt_bboxes_3d)
    input_meta = {'cam2img': cam2img}

    visualizer = Det3DLocalVisualizer()

    img = mmcv.imread(png_dir)
    img = mmcv.imconvert(img, 'bgr', 'rgb')
    visualizer.set_image(img)
    # project 3D bboxes to image
    visualizer.draw_proj_bboxes_3d(gt_bboxes_3d, input_meta)
    visualizer.show()
