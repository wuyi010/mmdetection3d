
"""

python tools/create_data.py kitti --root-path ./data/kitti --out-dir ./data/kitti --extra-tag kitti



python projects/BEVFusion/demo/multi_modality_demo.py demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin demo/data/nuscenes/ demo/data/nuscenes/n015-2018-07-24-11-22-45+0800.pkl projects/BEVFusion/configs/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d.py /home/didi/mmdetection3d/checkpoints/bevfusion_lidar-cam_voxel0075_second_secfpn_8xb4-cyclic-20e_nus-3d-fixed.pth --cam-type all --score-thr 0.2 --show

"""

"""
python tools/create_data.py kitti --root-path ./data/kitti --out-dir ./data/kitti --extra-tag kitti

python demo/pcd_demo.py /home/didi/mmdetection3d/demo/data/kitti/000000.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth 
python demo/pcd_demo.py /home/didi/mmdetection3d/demo/data/kitti/000000.bin configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-car.py checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-car_20220331_134606-d42d15ed.pth  --show



python demo/multi_modality_demo.py demo/data/kitti/000008.bin demo/data/kitti/000008.png demo/data/kitti/000008.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2 --out-dir ./outputs
python demo/multi_modality_demo.py demo/data/kitti/000008.bin demo/data/kitti/000008.png demo/data/kitti/000008.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2 --show --out-dir ./outputs
python demo/multi_modality_demo.py demo/data/kitti/000008.bin demo/data/kitti/000008.png demo/data/kitti/000008.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2  --show  --out-dir ./outputs --print-result



python demo/multi_modality_demo.py demo/data/kitti/000000.bin demo/data/kitti/000000.png demo/data/kitti/000000.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2  --out-dir ./outputs
python demo/multi_modality_demo.py demo/data/kitti/000000.bin demo/data/kitti/000000.png demo/data/kitti/000000.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2 --show --out-dir ./outputs
python demo/multi_modality_demo.py demo/data/kitti/000000.bin demo/data/kitti/000000.png demo/data/kitti/000000.pkl configs/mvxnet/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class.py checkpoints/mvxnet_fpn_dv_second_secfpn_8xb2-80e_kitti-3d-3class-fixed.pth --cam-type CAM2 --show --out-dir ./outputs --print-result




"""