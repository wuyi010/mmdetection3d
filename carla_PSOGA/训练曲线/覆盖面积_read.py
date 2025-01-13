import re
import matplotlib.pyplot as plt
import seaborn as sns
# 文件路径
log_file = '/home/didi/mmdetection3d_ing/carla_PSOGA/训练曲线/data.log'

# 初始化存储数据的字典
acc_data = {}

# 读取文件并提取Acc数据
with open(log_file, 'r') as file:
    lines = file.readlines()
    count = 0
    for line in lines:
        # 使用正则表达式提取Acc字段
        match = re.search(r'Acc:(\d+\.\d+)', line)
        if match:
            acc_value = float(match.group(1))
            acc_data[count] = acc_value
            count += 1

# 打印提取的Acc数据
# print(acc_data)

# 定义数据列表，提取前 1000 个或最多 len(acc_data) 个
use_acc = [acc_data[i] for i in range(min(1000, len(acc_data)))]

data = use_acc

# 提取横坐标和纵坐标
x_values = list(range(len(data)))
y_values = [value * 2 for value in data]  # y值增大1500倍





# 设置横坐标稀疏化（每隔10个点显示一个）
x = x_values[::15]  # 每10个数据点选一个
y = y_values[::15]  # 每10个数据点选一个

print(x)
print(y)
# 绘制图形
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='.',
         linestyle='--', #values are '-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'
         color='b',
         markersize=8,
         markerfacecolor='r',
         markeredgewidth=2,)

# 设置x轴和y轴标签
# 设置网格线
plt.grid(True, which='both', linestyle='--', linewidth=0.1)

# 设置x轴和y轴标签
plt.xlabel('Iteration', fontsize=12, fontweight='bold')
plt.ylabel('Average Coverage Area / m$^3$', fontsize=12, fontweight='bold')

# 显示图形
plt.show()



# 461.479, 575.761, 538.092, 589.112, 688.45, 618.42, 673.853, 667.461, 663.866, 694.901, 773.755, 642.541, 713.201, 714.025, 780.181,
