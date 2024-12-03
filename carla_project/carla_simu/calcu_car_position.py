import math

# 定义卡车的坐标
x1, y1 = 384.457947, -66.369019
x2, y2 = 384.963806, -132.471375

# 计算两点间的距离
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# 分成7段 (6个点)
num_segments = 7

# 计算每段的变化量
dx = (x2 - x1) / num_segments
dy = (y2 - y1) / num_segments

# 计算并打印中间的6个点, 保留小数点前6位
points = []
for i in range(1, num_segments):
    x_i = round(x1 + i * dx, 6)
    y_i = round(y1 + i * dy, 6)
    points.append((x_i, y_i))

# 打印中间的6个点
for idx, (x, y) in enumerate(points, start=1):
    print(f"Point {idx}: (x={x}, y={y})")
