import numpy as np

# 定义 Box 的参数
box = [0, 0, 0.8, 4.0, 1.8, 1.6, 0.3]  # [x_center, y_center, z_center, length, width, height, yaw_angle]
x_c, y_c, z_c, length, width, height, yaw = box

# 定义旋转矩阵，绕z轴旋转
def get_rotation_matrix(yaw_angle):
    cos_angle = np.cos(yaw_angle)
    sin_angle = np.sin(yaw_angle)
    return np.array([[cos_angle, -sin_angle, 0],
                     [sin_angle,  cos_angle, 0],
                     [0,           0,        1]])

# 判断点是否在box内
def is_point_in_box(point, box):
    # 提取 box 参数
    x_c, y_c, z_c, length, width, height, yaw = box

    # 平移点，使盒子中心在原点
    point_translated = point - np.array([x_c, y_c, z_c])

    # 获取旋转矩阵
    rotation_matrix = get_rotation_matrix(-yaw)  # 逆时针旋转，逆向旋转回去

    # 旋转点，使得box对齐
    point_rotated = np.dot(rotation_matrix, point_translated)

    # 判断点是否在标准轴对齐的box范围内
    in_x = -length / 2 <= point_rotated[0] <= length / 2
    in_y = -width / 2 <= point_rotated[1] <= width / 2
    in_z = -height / 2 <= point_rotated[2] <= height / 2

    return in_x and in_y and in_z

# 测试点
points = np.array([[ 0.19525402,  0.86075747,  0.7190158 ],
                   [ 0.4110535,   0.17953273,  0.87406391],
                   [-0.3053808,   0.58357645,  1.39526239],
                   [-0.24965115 , 1.567092,    0.12045094],
                   [ 1.85465104 ,-0.46623392 , 1.33353343],
                   [ 1.16690015,  0.11557968,  1.34127574]])

# 判断每个点是否在 Box 内
for point in points:
    result = is_point_in_box(point, box)
    print(f"Point {point} in box: {result}")
