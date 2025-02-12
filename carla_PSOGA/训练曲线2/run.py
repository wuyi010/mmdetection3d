import os

# 指定目标目录
target_dir = "/home/didi/mmdetection3d_ing/carla_PSOGA/训练曲线2"

# 遍历目标目录下的所有文件
for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            print(f"正在运行 {file_path} ...")
            os.system(f'python {file_path}')