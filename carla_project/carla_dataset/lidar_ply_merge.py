import math
import os
import re

import carla_run
import numpy as np


# 获取指定目录下所有 PLY 文件
def get_ply_files(directory):
    # 获取所有以 .ply 结尾的文件
    ply_files = [f for f in os.listdir(directory) if f.endswith('.ply')]

    # 自定义排序规则，提取文件名中的 - 前数字和 L 后数字
    def sort_key(file_name):
        match = re.match(r'(\d+)-L(\d+)', file_name)  # 匹配类似 879583-L1, 879583-L2 的文件名
        if match:
            # 按照两个部分排序，先按 - 之前的数字，再按 L 后面的数字
            return int(match.group(1)), int(match.group(2))
        return float('inf'), float('inf')  # 没有匹配到的文件放在最后

    # 按照自定义的排序规则进行排序
    sorted_ply_files = sorted(ply_files, key=sort_key)
    return sorted_ply_files


