
import pandas as pd
import matplotlib.pyplot as plt
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import make_interp_spline


# 启用 Seaborn 风格
sns.set(style="whitegrid")
# 读取Excel文件

df = pd.read_excel('data.xlsx')
x = df['x']

to_rad = 0.017453292519943295
CAM_I_FR =  df['CAM_I_FR_YAW']  * to_rad
CAM_I_BR = df['CAM_I_BR_YAW'] * to_rad
CAM_II   = df['CAM_II_YAW'] * to_rad

LIDAR_I_FR =  df['LIDAR_I_FR_YAW'] * to_rad
LIDAR_I_BR =  df['LIDAR_I_BR_YAW'] * to_rad
LIDAR_II_R =  df['LIDAR_II_R_YAW'] * to_rad
LIDAR_II_F =  df['LIDAR_II_F_YAW'] * to_rad

RADAR_FR = df['RADAR_FR_YAW'] * to_rad
RADAR_BR = df['RADAR_BR_YAW'] * to_rad
RADAR_F  =  df['RADAR_F_YAW'] * to_rad
# 设置绘图风格
plt.figure(figsize=(10,8))
"""
 '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
 
'b': 蓝色（blue）'g': 绿色（green）'r': 红色（red）'c': 青色（cyan）'m': 品红（magenta）
'y': 黄色（yellow）'k': 黑色（black）'w': 白色（white）

'.': 点 ',': 像素点 'o': 圆圈'v': 倒三角'^': 正三角'<': 左三角'>': 右三角
'1': 三叉标记（下）'2': 三叉标记（上）'3': 三叉标记（左）'4': 三叉标记（右's': 正方'p': 五边形
'*': 星号'h': 六边形1'H': 六边形2'+': 加号'x': 叉号'D': 菱形'd': 小菱形 '|': 垂直线 '_': 水平线
"""
#摄像头 0 45 135
plt.plot(x, CAM_I_FR, marker='', linestyle='solid', color='r', label='CAM_I_FR')  #
plt.plot(x, CAM_I_BR, marker='', linestyle='solid', color='g', label='CAM_I_BR')  #
plt.plot(x, CAM_II, marker='', linestyle='solid', color='b', label='CAM_II')  #
#LIDAR I 30 120
plt.plot(x, LIDAR_I_FR, marker='', linestyle='--', color='c', label='LIDAR_I_FR')  #
plt.plot(x, LIDAR_I_BR, marker='', linestyle='--', color='m', label='LIDAR_I_BR')  #
#LIDAR II 0  (110,-50,-15)
plt.plot(x, LIDAR_II_R, marker='', linestyle='--', color='k', label='LIDAR_II_R')  # 绘制平滑曲线 y1
plt.plot(x, LIDAR_II_F, marker='', linestyle='--', color='y', label='LIDAR_II_F')  # 绘制平滑曲线 y2
#毫米波雷达
plt.plot(x, RADAR_FR, marker='', linestyle='dotted', color='r', label='RADAR_FR')  # 绘制平滑曲线 y1
plt.plot(x, RADAR_BR, marker='', linestyle='dotted', color='g', label='RADAR_BR')  # 绘制平滑曲线 y2
plt.plot(x, RADAR_F, marker='', linestyle='dotted', color='b', label='RADAR_F')  # 绘制平滑曲线 y2


plt.grid(True, which='both', linestyle='--', linewidth=0.1)
# 设置x轴和y轴标签
plt.xlabel('Number of Iterations', fontsize=16, fontweight='normal')
plt.ylabel('The Yaw Mounting Angle / rad', fontsize=16, fontweight='normal')

# 添加图例
plt.legend(fontsize=14)

# 去除顶部和右侧边框
sns.despine()
# 获取当前 Python 文件的文件名（不包括扩展名）
filename = os.path.splitext(os.path.basename(__file__))[0]
# 保存图像到目录
plt.savefig(f"image/{filename}", dpi=300, bbox_inches='tight')  # 将路径替换为实际保存路径

# # 显示图形
plt.show()




