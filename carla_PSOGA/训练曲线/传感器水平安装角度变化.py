import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import make_interp_spline

# 数据
x = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
scaled_x = [xi * 200 / 1000 for xi in x]
x =  [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0]
print(scaled_x)
y1 = [1.6, 1.5, -1.2, -1.1 ,1.3526 ,-1.165 ,0.714918 ,-0.581778, -0.315586, -0.46467,-0.372916, -0.2, -0.1, 0, 0, 0, 0, 0, 0, 0, 0]
y2 = [-1.2, -1, 1.1, 0 ,0.6 ,1.2 ,1.1 ,0.9, 0.7, 0.75,0.86, 0.85, 0.78, 0.84, 0.83,0.80, 0.837, 0.837, 0.837, 0.837, 0.837]
y3 = [-1.5, -1, 0, 0.2 ,0.4 ,0.6 ,0.84 ,0.85, 0.9, 1.2,1.4, 1.5, 1.8, 1.9, 2.024,2.0, 2.024, 2.024, 2.024, 2.024, 2.024]

z1 = [2.06, 1.825, -1.6, 1.5 ,-1.4 ,1.0 ,-0.8345 ,0.581778, -0.315586, 0.35,-0.372916, 0.5, -0.08, 0.04, -0.081, 0.04, 0.02, 0.01, 0.0, 0.01, 0.01]
z2 = [-1.8, -1.1, -0.5, 0 ,0.2 ,0.28 ,0.4 ,0.3, 1.2, 1.0,0.9, 0.5, 0.88, 0.4,0.7,0.75, 0.7853, 0.7853,0.7853, 0.7853, 0.7853]
z3 = [2.5, 2.643, 2.4, 1.8, 2.0 ,2.77 ,1.495 ,2.5 ,1.8, 1.99, 2.01,2.398, 2.12, 2.2, 2.3562, 2.3562,2.3562, 2.3562, 2.3562, 2.3562, 2.3562]
# 使用样条插值进行平滑
spl1   = make_interp_spline(x, y1, k=1)  # 对 y1 进行插值
spl2   = make_interp_spline(x, y2, k=1)  # 对 y2 进行插值
spl3   = make_interp_spline(x, y3, k=1)  # 对 y2 进行插值
z_spl1 = make_interp_spline(x, z1, k=1)  # 对 y1 进行插值
z_spl2 = make_interp_spline(x, z2, k=1)  # 对 y2 进行插值
z_spl3 = make_interp_spline(x, z3, k=1)  # 对 y2 进行插值
x_new = np.linspace(min(x), max(x), 500)  # 生成更多的 x 值
y1_new = spl1(x_new)
y2_new = spl2(x_new)
y3_new = spl3(x_new)
z1_new = z_spl1(x_new)
z2_new = z_spl2(x_new)
z3_new = z_spl3(x_new)

# 设置绘图风格
plt.figure(figsize=(10, 6))
plt.plot(x_new, y1_new, marker='', linestyle='-', color='r', label='LiDar_FRONT')  # 绘制平滑曲线 y1
plt.plot(x_new, y2_new, marker='', linestyle='-', color='b', label='LiDar_FRONT_RIGHT')  # 绘制平滑曲线 y2
plt.plot(x_new, y3_new, marker='', linestyle='-', color='g', label='LiDar_BACK_RIGHT')  # 绘制平滑曲线 y2
# 添加虚线 z1, z2, z3
plt.plot(x_new, z1_new, linestyle='--', color='c', label='CAM_FRONT')  # 绘制 z1 曲线
plt.plot(x_new, z2_new, linestyle='--', color='m', label='CAM_FRONT_RIGHT')  # 绘制 z2 曲线
plt.plot(x_new, z3_new, linestyle='--', color='y', label='CAM_BACK_RIGHT')  # 绘制 z3 曲线
# 设置网格线
plt.grid(True, which='both', linestyle='--', linewidth=0.2)

# 设置x轴和y轴标签
plt.xlabel('Iteration', fontsize=12, fontweight='bold')
plt.ylabel('The Horizontal Mounting Angle of The Sensor Changes / rad', fontsize=12, fontweight='bold')

# 添加图例
plt.legend()

# 去除顶部和右侧边框
sns.despine()
# 获取当前 Python 文件的文件名（不包括扩展名）
filename = os.path.splitext(os.path.basename(__file__))[0]
# 保存图像到目录
plt.savefig(f"{filename}", dpi=300, bbox_inches='tight')  # 将路径替换为实际保存路径

# 显示图形
plt.show()


a  = [-1.077042 -0.923816 -0.821774 -0.714918 -0.581778 -0.315586 -0.46467,-0.372916]
b =np.array(a)-2
print(b[::-1])
print(135*np.pi/180)

