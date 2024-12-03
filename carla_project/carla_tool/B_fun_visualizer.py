import time
import torch
import open3d as o3d
from matplotlib import pyplot as plt
import mmcv
import numpy as np
from mmengine import load

from carla_project.carla_tool.draw_bboxes_3d import draw_bboxes_3d
from mmdet3d.structures import CameraInstance3DBoxes
from mmdet3d.visualization import Det3DLocalVisualizer
from mmdet3d.structures import LiDARInstance3DBoxes

def demo_visualizer_bboxes_3d_one():
    # 定义3D边界框
    bbox_data = [
        [0, 0, 0, 0.1, 0.1, 0.1, 0],
        [3.5054702758789062, -3.404402494430542, -1.9501473903656006, 4.452672004699707, 1.6548149585723877, 1.4870104789733887, 0.09145307540893555], [3.3534655570983887, 3.2845494747161865, -1.860813856124878, 4.36966609954834, 1.6892982721328735, 1.4939353466033936, -0.04569685459136963], [26.663057327270508, 3.3974437713623047, -1.912292242050171, 3.6368186473846436, 1.5778532028198242, 1.4421439170837402, -0.10897934436798096],
        [
            3.3960418701171875, -3.4237451553344727, -1.9010233879089355, 4.390101432800293, 1.6461946964263916, 1.458119511604309, 0.10135328769683838],
        [3.428109884262085, 3.289954900741577, -1.9288091659545898, 4.512115001678467, 1.7446749210357666,
         1.553249478340149, -0.024068117141723633],
        [1.6456098556518555, -16.013309478759766, -1.9793099164962769, 3.48288893699646, 1.4510301351547241,
         1.3681306838989258, 1.8876625299453735],
        [26.825212478637695, -3.1417734622955322, -1.9601402282714844, 3.5642495155334473, 1.566406011581421,
         1.4477444887161255, 0.10867583751678467],
        [24.91574478149414, -12.102263450622559, -1.9775407314300537, 4.279739856719971, 1.6864948272705078, 1.4863530397415161, -1.5579220056533813], [26.884252548217773, 3.456390857696533, -1.8918430805206299, 3.9123198986053467, 1.604655146598816, 1.4629229307174683, -0.049666404724121094], [26.936168670654297, -3.2638046741485596, -1.9241293668746948, 4.049038887023926, 1.6271082162857056, 1.4763798713684082, 0.09675848484039307], [3.450681209564209, -3.4225594997406006, -1.939399242401123, 4.400033473968506, 1.6526468992233276, 1.4759212732315063, 0.10226821899414062], [3.465395927429199, 3.2880961894989014, -1.9481680393218994, 4.560767650604248, 1.7574526071548462, 1.5659412145614624, -0.016752958297729492],
        [26.936237335205078, 3.4454421997070312, -1.8792392015457153, 4.041769981384277, 1.6026185750961304,
         1.4586071968078613, -0.03747749328613281],
        [3.459650754928589, -3.4074583053588867, -1.9451419115066528, 4.358723163604736, 1.6619364023208618,
         1.5403828620910645, 0.08714473247528076],
        [3.4935975074768066, 3.270526885986328, -1.9513142108917236, 4.512984275817871, 1.7425146102905273,
         1.5632380247116089, 4.57763671875e-05],
        [26.8271541595459, -3.1497650146484375, -1.960004210472107, 3.5653631687164307, 1.5665663480758667,
         1.4488015174865723, 0.10320305824279785],
        [24.910390853881836, -12.096457481384277, -1.9934524297714233, 4.292566299438477, 1.6939224004745483,
         1.4918289184570312, -1.5582176446914673],
        [26.946048736572266, -3.2880403995513916, -1.9295403957366943, 4.057748794555664, 1.6260960102081299,
         1.4829425811767578, 0.06556820869445801],
        [3.5173563957214355, -3.3970625400543213, -1.9324626922607422, 4.4421162605285645, 1.659173846244812,
         1.484776258468628, 0.09315228462219238],
        [3.62296199798584, 3.1727304458618164, -1.9649380445480347, 4.242929458618164, 1.6670818328857422,
         1.706299066543579, 0.06539714336395264],
        [26.662967681884766, 3.397712469100952, -1.9122612476348877, 3.636322498321533, 1.5781556367874146,
         1.4425002336502075, -0.10809135437011719],

    ]
    bin_dir_sim = "/home/didi/mmdetection3d/carla_project/Carla_data/dataset/points/000025.bin"
    bin_path = '/home/didi/mmdetection3d/demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin'
    draw_bboxes_3d(bbox_data, bin_dir_sim)


def visualize_bboxes_3d_carla(base_dir="/home/didi/mmdetection3d/carla_project"):
    import os
    import json

    # 定义目录和范围

    from carla_project.A0_config import dataset_list_name_list
    camera_dirs = dataset_list_name_list[:5]
    preds_subdir = "preds"


    folder_path = os.path.join(base_dir, 'dataset/points')
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    file_range = range(file_count)  # 对应从000000到000030


    # 遍历每个目录和文件
    # Vehicledimensions = Length = 7.94, Width = 2.89, Height = 3.46
    ego = [0, 0, -2, 7.94, 2.89, 3.46, 0]
    point_center = [0, 0, -2, 0.1, 0.1, 0.1, 0]
    folder_path_outputs = os.path.join(base_dir, 'outputs')
    for i in file_range:
        # i= input_which_one
        bboxes_3d_list = []
        bboxes_3d_list.append(ego)
        bboxes_3d_list.append(point_center)

        for camera_dir in camera_dirs:
            # 构建文件路径，例如：carla_project/outputs/CAM_BACK_LEFT/preds/000000.json
            file_path = os.path.join(folder_path_outputs, camera_dir, preds_subdir, f"{i:06d}.json")
            print(file_path,end="\t\t")
            # 检查文件是否存在
            if os.path.exists(file_path):
                # 打开并读取JSON文件
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # 提取bboxes_3d的值，并添加到列表中
                    bboxes_3d = data.get('bboxes_3d', [])
                    print(f"提取的bboxes_3d数量: {len(bboxes_3d)}")
                    # print(bboxes_3d)
                    bboxes_3d_list.extend(bboxes_3d)  # 将bboxes_3d的二维数组添加到总列表中
            else:
                print(f"文件 {file_path} 不存在，跳过")

        print(f"提取的bboxes_3d数量: {len(bboxes_3d_list)}")
        print(bboxes_3d_list)
        scores = torch.tensor([0.9, 0.85])  # 替换为你的置信度分数
        iou_threshold = 0.5  # 你可以根据需要调整这个值
        from torchvision.ops import nms# 进行非极大值抑制
        keep_indices = nms(bboxes_3d_list, scores, iou_threshold)

        # 保留去除重复框后的框
        filtered_bboxes = bboxes_3d_list[keep_indices]
        filtered_scores = scores[keep_indices]



        # print(bboxes_3d_list)
        bin_dir_sim = f"{folder_path}/{i:06d}.bin"
        draw_bboxes_3d(filtered_bboxes, bin_dir_sim)



def is_same_object(box1, box2, position_threshold=0.5, size_threshold=0.5, ):
    # 根据位置和尺寸的相似性判断两个框是否代表同一个物体
    center_dist = np.linalg.norm(np.array(box1[:3]) - np.array(box2[:3]))  # 计算3D空间中两个框的中心距离
    size_dist = np.linalg.norm(np.array(box1[3:6]) - np.array(box2[3:6]))  # 计算框的尺寸差异
    # print("position_diff, size_diff", center_dist, size_dist)
    return center_dist < position_threshold and size_dist < size_threshold

def carla_vis_nms(base_dir="/home/didi/mmdetection3d/carla_project"):

    import os
    import json
    # 定义目录和范围
    from carla_project.A0_config import dataset_list_name_list
    camera_dirs = dataset_list_name_list[:5]
    preds_subdir = "preds"

    folder_path = os.path.join(base_dir, 'dataset/points')
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    file_range = range(file_count)  # 对应从000000到000030
    print(file_range)


    # 遍历每个目录和文件
    # Vehicledimensions = Length = 7.94, Width = 2.89, Height = 3.46
    ego = [0, 0, -2, 7, 2.6, 3.46, 0]
    point_center = [0, 0, -2, 0.05, 0.05, 0.05, 0]
    folder_path_outputs = os.path.join(base_dir, 'outputs')

    position_threshold = 0.6  # 位置差异的阈值    # 定义阈值，用于判断两个框是否是重复的 (可以调整这个阈值)
    size_threshold = 0.4  # 尺寸差异的阈值

    for i in file_range:
        # i= input_which_one
        all_labels = []
        all_scores = []
        all_bboxes = []

        # 定义预测结果文件路径
        file_paths=[]
        for camera_dir in camera_dirs:
            file_path = os.path.join(folder_path_outputs, camera_dir, preds_subdir, f"{i:06d}.json")
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
        bin_dir_sim = os.path.join(folder_path,  f"{i:06d}.bin")
        print(f"当前图像:",  f"{i:06d}.bin")
        draw_bboxes_3d(final_bboxes, bin_dir_sim)






if __name__ == "__main__":

    # draw_proj_bboxes_3d(pkl_dir = "/home/didi/mmdetection3d/data/kitti/testing/pkl/000000.pkl",
    #                     png_dir = "/home/didi/mmdetection3d/data/kitti/testing/image_2/000000.png")

    # draw_points_on_image(name='000000')

    # draw_bboxes_3d("/home/didi/mmdetection3d/demo/data/kitti/备份_kitti/000008.bin")


    # visualize_bboxes_3d_carla("/home/didi/mmdetection3d/carla_project/Carla_data_map4_plan1")

    # carla_vis_nms("/home/didi/mmdetection3d/carla_project/Carla_data_map4_plan1")

    # carla_vis_nms("/home/didi/mmdetection3d/carla_project/Carla_data_test_1120")


    carla_vis_nms("/home/didi/mmdetection3d/carla_project/Carla_data")

    # carla_vis_nms("/carla_project/Carla_data_map4_plan1_vehicle")
    # carla_vis_nms("/carla_project/Carla_data_map3_plan1_vehicle")
    # carla_vis_nms("/home/didi/mmdetection3d/carla_project/Carla_data_map4_plan2_vehicle")
    # carla_vis_nms("/home/didi/mmdetection3d/carla_project/Carla_data_map4_plan1_vehicle")




