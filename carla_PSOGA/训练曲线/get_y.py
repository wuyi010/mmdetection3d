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

LiDAR_F= df['LiDAR-F-Y']
LIDAR_FR = df['LIDAR_FR_Y']
LIDAR_BR = df['LIDAR_BR_Y']

CAM_I_FR = df['CAM-I-FR-Y']
CAM_I_BR = df['CAM-I-BR-Y']
CAM_II_FR = df['CAM-II-FR-Y']



# 设置绘图风格
plt.figure(figsize=(9, 6))
"""
 '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'

'b': 蓝色（blue）'g': 绿色（green）'r': 红色（red）'c': 青色（cyan）'m': 品红（magenta）
'y': 黄色（yellow）'k': 黑色（black）'w': 白色（white）

'.': 点 ',': 像素点 'o': 圆圈'v': 倒三角'^': 正三角'<': 左三角'>': 右三角
'1': 三叉标记（下）'2': 三叉标记（上）'3': 三叉标记（左）'4': 三叉标记（右's': 正方'p': 五边形
'*': 星号'h': 六边形1'H': 六边形2'+': 加号'x': 叉号'D': 菱形'd': 小菱形 '|': 垂直线 '_': 水平线
"""
# 摄像头 0 45 135
plt.plot(x, LIDAR_FR, marker='', linestyle='solid', color='r', label='LIDAR_FR')  #
plt.plot(x, LIDAR_BR, marker='', linestyle='solid', color='g', label='LIDAR_BR')  #
plt.plot(x, LiDAR_F, marker='', linestyle='solid', color='b', label='LiDAR_F')  #
# LIDAR I 30 120
plt.plot(x, CAM_I_FR, marker='', linestyle='--', color='c', label='CAM_I_FR')  #
plt.plot(x, CAM_I_BR, marker='', linestyle='--', color='m', label='CAM_I_BR')  #
plt.plot(x, CAM_II_FR, marker='', linestyle='dotted', color='r', label='CAM_II_FR')  # 绘制平滑曲线 y1


plt.grid(True, which='both', linestyle='--', linewidth=0.1)
# 设置x轴和y轴标签
plt.xlabel('Number of Iterations', fontsize=16, fontweight='normal')
plt.ylabel('Y-axis / m', fontsize=16, fontweight='normal')

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





