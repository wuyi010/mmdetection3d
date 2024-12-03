import re
import time

from matplotlib import image as mpimg

import os
import math
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

def display_png_images(png_directory, delay=1):
    # 获取所有 .png 文件
    png_files = [f for f in os.listdir(png_directory) if f.endswith('.png')]

    if not png_files:
        print("No PNG files found in the directory.")
        return

    # 按文件名排序，确保数字排序
    png_files.sort(key=lambda f: int(f.split('.')[0]))  # 假设文件名格式为 '346819.png'
    print(png_files)
    # 循环显示每个图像
    for png_file in png_files:
        img_path = os.path.join(png_directory, png_file)
        print(f"Displaying: {img_path}")

        # 加载图像
        img = mpimg.imread(img_path)
        plt.imshow(img)
        plt.axis('off')  # 隐藏坐标轴
        plt.show()

        # 暂停指定的时间（单位：秒）
        time.sleep(delay)

        # 关闭当前图像窗口
        plt.close()


if __name__ == "__main__":
    display_png_images("/home/didi/mmdetection3d/carla_project/outputs/vis_camera/CAM2")