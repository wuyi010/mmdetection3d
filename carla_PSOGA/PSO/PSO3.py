import os
import numpy as np
import matplotlib.pyplot as plt

# 定义目标函数（此处为简单的二次函数）
def objective_function(x):
    return x[0] ** 2 + x[1] ** 2

# 粒子类
class Particle:
    def __init__(self, x0):
        self.position = np.array(x0)  # 初始化位置
        self.velocity = np.random.rand(len(x0))  # 初始化速度
        self.best_position = self.position.copy()  # 个人最佳位置
        self.best_value = objective_function(self.position)  # 个人最佳位置对应的目标函数值

    def update_velocity(self, global_best_position, w, c1, c2):
        r1, r2 = np.random.rand(2)
        cognitive_component = c1 * r1 * (self.best_position - self.position)
        social_component = c2 * r2 * (global_best_position - self.position)
        self.velocity = w * self.velocity + cognitive_component + social_component

    def update_position(self, bounds):
        self.position += self.velocity
        # 边界约束
        for i in range(len(self.position)):
            if self.position[i] > bounds[i][1]:
                self.position[i] = bounds[i][1]
            if self.position[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]

        # 更新个人最佳位置
        current_value = objective_function(self.position)
        if current_value < self.best_value:
            self.best_value = current_value
            self.best_position = self.position.copy()

# 粒子群优化算法类
class PSO:
    def __init__(self, objective_function, bounds, num_particles, max_iter, w=0.9, c1=1.5, c2=1.5):
        self.objective_function = objective_function
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.w = w  # 惯性权重
        self.c1 = c1  # 认知常数
        self.c2 = c2  # 社会常数
        self.particles = [Particle(np.random.uniform(low, high, len(bounds))) for low, high in bounds]
        self.global_best_position = None
        self.global_best_value = float('inf')

    def optimize(self):
        # 初始化 global_best_position 为第一个粒子的最佳位置
        self.global_best_position = self.particles[0].best_position

        plt.ion()  # 开启交互模式

        for iter_count in range(self.max_iter):
            for particle in self.particles:
                # 更新粒子的速度
                particle.update_velocity(self.global_best_position, self.w, self.c1, self.c2)
                # 更新粒子的位置
                particle.update_position(self.bounds)

                # 更新全局最佳位置
                if particle.best_value < self.global_best_value:
                    self.global_best_value = particle.best_value
                    self.global_best_position = particle.best_position

            # 每次迭代更新粒子的位置
            self.plot_particles(iter_count)

            print(f"Iteration {iter_count + 1}, Global Best Position: {self.global_best_position}, Global Best Value: {self.global_best_value}")

        plt.ioff()  # 关闭交互模式
        plt.show()

        return self.global_best_position, self.global_best_value

    def plot_particles(self, iter_count):
        plt.clf()  # 清空当前图像
        positions = np.array([particle.position for particle in self.particles])
        plt.scatter(positions[:, 0], positions[:, 1], color='blue', label='Particles')
        plt.scatter(self.global_best_position[0], self.global_best_position[1], color='red', label='Global Best', marker='*', s=200)
        plt.xlim(self.bounds[0])
        plt.ylim(self.bounds[1])
        plt.title(f'Iteration {iter_count + 1}')
        plt.legend()
        plt.draw()  # 绘制图像
        plt.pause(0.2)  # 暂停以便更新图像

def PSO_Find_the_minimum_value_of_a_quadratic_function():
    # 参数设置
    bounds = [(-10, 10), (-10, 10)]  # 搜索空间的边界
    num_particles = 1000  # 粒子数量
    max_iter = 100  # 最大迭代次数

    # 实例化PSO并运行优化
    pso = PSO(objective_function, bounds, num_particles, max_iter)
    best_position, best_value = pso.optimize()

    print(f"\nBest Position: {best_position}")
    print(f"Best Value: {best_value}")

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    PSO_Find_the_minimum_value_of_a_quadratic_function()

"""
代码解析：
plt.ion(): 开启交互模式，允许动态更新图像。
plt.clf(): 在每次绘制新图像之前清除当前图像，使得新的图像可以在同一窗口中显示。
plt.draw(): 绘制图像并在屏幕上显示更新。
plt.pause(0.1): 暂停 0.1 秒，以便显示图像更新。你可以调整这个值来控制图像刷新速度。
这样，在每次迭代时，你都能看到所有粒子的位置动态更新，并且整个过程会在同一个图像窗口中呈现。
0915
"""