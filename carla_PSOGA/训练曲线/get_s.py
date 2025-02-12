import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import make_interp_spline
import os

# 启用 Seaborn 风格
sns.set(style="whitegrid")

# 读取Excel文件
df = pd.read_excel('data.xlsx')
x = df['x']
s = df['s']  # 假设该列存在

# 设置绘图风格
plt.figure(figsize=(9, 6))

# 摄像头 0 45 135
plt.plot(x, s,
         marker='o',
         linestyle='--',
         color='b',
         markersize=2,
         markerfacecolor='r',
         markeredgewidth=2,
         label='volume')

plt.grid(True, which='both', linestyle='--', linewidth=0.1)

# 设置x轴和y轴标签

plt.xlabel('Number of Iterations', fontsize=16, fontweight='normal')
plt.ylabel('Actual volume / m³', fontsize=16, fontweight='normal')



final_value = 1348.4911
if len(x) > 81:  # 确保索引存在
    plt.text(x[80], final_value, f'Final Volume: {final_value:.2f} m³',
             fontsize=16, fontweight='normal', color='b',
             ha='center', va='bottom')

# 添加图例
plt.legend(fontsize=14)

# 去除顶部和右侧边框
sns.despine()
# 获取当前 Python 文件的文件名（不包括扩展名）
filename = os.path.splitext(os.path.basename(__file__))[0]
# 保存图像到目录
plt.savefig(f"image/{filename}", dpi=300, bbox_inches='tight')  # 将路径替换为实际保存路径

# 显示图形
plt.show()
