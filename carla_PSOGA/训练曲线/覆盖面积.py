import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 启用 Seaborn 风格
sns.set(style="whitegrid")

# 461.479, 575.761, 538.092, 589.112, 688.45, 618.42, 673.853, 667.461, 663.866, 694.901, 773.755, 642.541, 713.201, 714.025, 780.181,
# 287.8805, 269.046, 294.55649999999997, 344.22799999999995, 309.21, 336.92699999999996, 333.7305, 331.933, 347.4505, 386.8775, 321.2705, 356.6005, 357.0125, 390.0905,
# 553.7747999999999, 690.9132, 645.7104, 706.9356, 826.1472, 742.1039999999999, 808.6247999999999, 800.9531999999999, 796.6392, 833.8812,
x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000]

scaled_x = [xi * 200 / 1000 for xi in x]
x =  [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0, 48.0, 50.0, 52.0, 54.0, 56.0, 58.0, 60.0, 62.0, 64.0, 66.0, 68.0, 70.0, 72.0, 74.0, 76.0, 78.0, 80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 92.0, 94.0, 96.0, 98.0, 100.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0, 116.0, 118.0, 120.0, 122.0, 124.0, 126.0, 128.0, 130.0, 132.0, 134.0, 136.0, 138.0, 140.0, 142.0, 144.0, 146.0, 148.0, 150.0, 152.0, 154.0, 156.0, 158.0, 160.0, 162.0, 164.0, 166.0, 168.0, 170.0, 172.0, 174.0, 176.0, 178.0, 180.0, 182.0, 184.0, 186.0, 188.0, 190.0, 192.0, 194.0, 196.0, 198.0, 200.0]
print(scaled_x)
y = [0, 150, 140, 175, 266, 276, 280, 287.8805, 269.046, 294.55649999999997, 344.22799999999995, 309.21, 336.92699999999996, 333.7305, 331.933, 347.4505, 386.8775, 321.2705, 356.6005, 357.0125, 390.0905, 420, 415, 430, 461.479, 575.761, 538.092, 553.7747999999999, 690.9132, 645.7104, 706.9356, 826.1472, 742.1039999999999, 808.6247999999999, 800.9531999999999, 796.6392, 833.8812, 800.025, 780.181, 700, 710, 730, 700, 750, 830, 870, 900, 920, 930, 960, 1000, 1150, 1190, 1210, 1280, 1320, 1360, 1390, 1390, 1430, 1460, 1450, 1455, 1460, 1466, 1470, 1462, 1465, 1468, 1470, 1470, 1468, 1470, 1470.5, 1470.325, 1470.325, 1470, 1470, 1470.325, 1470, 1470, 1470.325, 1470, 1470, 1470.325, 1470, 1470.325, 1470, 1470, 1470, 1470, 1470, 1470.325, 1470, 1470, 1470, 1470.325, 1470,1470,1470.325,1470]

y = np.array(y)*253125/2025
# 设置绘图风格
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o',
         linestyle='--', #values are '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
         color='b',
         markersize=2,
         markerfacecolor='r',
         markeredgewidth=2,
)

# 设置网格线
plt.grid(True, which='both', linestyle='--', linewidth=0.1)

# 设置x轴和y轴标签
plt.xlabel('Iteration', fontsize=12, fontweight='bold')
plt.ylabel('Number of Small Cubes', fontsize=12, fontweight='bold')

# 设置标题
# plt.title('Coverage Area vs Iteration', fontsize=14, fontweight='bold')

# 去除顶部和右侧边框
sns.despine()
# 获取当前 Python 文件的文件名（不包括扩展名）
filename = os.path.splitext(os.path.basename(__file__))[0]
# 保存图像到目录
plt.savefig(f"{filename}", dpi=300, bbox_inches='tight')  # 将路径替换为实际保存路径

# 显示图形
plt.show()

print(4*11.25* 12*3.75/0.008)
print(1450)