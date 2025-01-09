import carla
import cv2
import numpy as np
import time

import pygame
from config import carla_config as config



class CustomTimer:
    def __init__(self):
        try:
            self.timer = time.perf_counter
        except AttributeError:
            self.timer = time.time

    def time(self):
        return self.timer()

class DisplayManager:
    def __init__(self, grid_size, window_size):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode(window_size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.grid_size = grid_size
        self.window_size = window_size
        self.sensor_list = []

    def get_window_size(self):
        return [int(self.window_size[0]), int(self.window_size[1])]

    def get_display_size(self):
        return [int(self.window_size[0]/self.grid_size[1]), int(self.window_size[1]/self.grid_size[0])]

    def get_display_offset(self, gridPos):
        dis_size = self.get_display_size()
        return [int(gridPos[1] * dis_size[0]), int(gridPos[0] * dis_size[1])]

    def add_sensor(self, sensor):
        self.sensor_list.append(sensor)

    def get_sensor_list(self):
        return self.sensor_list

    def render(self):
        if not self.render_enabled():
            return

        for s in self.sensor_list:
            s.render()

        pygame.display.flip()

    def destroy(self):
        for s in self.sensor_list:
            s.destroy()

    def render_enabled(self):
        return self.display != None

# SensorManager(world, display_manager, 'RGBCamera', carla_project.Transform(carla_project.Location(x=0, z=2.4), carla_project.Rotation(yaw=-90)), vehicle, {}, display_pos=[0, 0])
class SensorManager:
    def __init__(self, world, display_man, sensor_type, transform, attached, sensor_options, display_pos, sensor_name):
        self.sensor_name = sensor_name
        self.surface = None
        self.world = world
        self.display_man = display_man
        self.display_pos = display_pos
        self.sensor = self.init_sensor(sensor_type, transform, attached, sensor_options, sensor_name)
        self.sensor_options = sensor_options
        self.timer = CustomTimer()
        self.point_cloud_data = []  # 存储接收到的点云数据
        self.frame_collected = 0  # 用于统计收集到的雷达帧数

        self.time_processing = 0.0
        self.tics_processing = 0

        self.display_man.add_sensor(self)

    def init_sensor(self, sensor_type, transform, attached, sensor_options,sensor_name):
        if sensor_type == 'RGBCamera':
            camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')

            disp_size = self.display_man.get_display_size()


            save_size = config.SensorCamera_set[sensor_name]['config']['resolution']
            camera_bp.set_attribute('image_size_x', str(save_size['W']))
            camera_bp.set_attribute('image_size_y', str(save_size['H']))

            for key in sensor_options:
                camera_bp.set_attribute(key, sensor_options[key])

            camera = self.world.spawn_actor(camera_bp, transform, attach_to=attached)
            camera.listen(lambda image:(
                self.save_rgb_image(image), # 调用原来的保存函数
                print(f'{config.CarlaDataPath["camera_path"]}/{self.sensor_name}_%.10d.png' % image.frame),
                image.save_to_disk(f'{config.CarlaDataPath["camera_path"]}/{self.sensor_name}_%.10d.png' % image.frame)))# 保存图像到磁盘
            return camera

        elif sensor_type == 'LiDAR':
            lidar_bp = self.world.get_blueprint_library().find('sensor.lidar.ray_cast')
            for key in sensor_options:
                lidar_bp.set_attribute(key, sensor_options[key])

            lidar = self.world.spawn_actor(lidar_bp, transform, attach_to=attached)
            lidar.listen(lambda point_cloud:(
                self.save_lidar_image(point_cloud),
                point_cloud.save_to_disk(f'{config.CarlaDataPath["lidar_path"]}/{self.sensor_name}_%.10d.ply' % point_cloud.frame) ))
            return lidar

        elif sensor_type == 'SemanticLiDAR':
            lidar_bp = self.world.get_blueprint_library().find('sensor.lidar.ray_cast_semantic')
            lidar_bp.set_attribute('range', '100')

            # 输出所有可用属性
            # print("Available LIDAR sensor attributes:")
            # for attribute in lidar_bp:
            #     print(attribute.id)



            for key in sensor_options:
                lidar_bp.set_attribute(key, sensor_options[key])

            lidar = self.world.spawn_actor(lidar_bp, transform, attach_to=attached)

            # lidar.listen(self.save_semanticlidar_image)

            lidar.listen(lambda point_cloud: (
                self.save_semanticlidar_image,
                point_cloud.save_to_disk(f'{config.CarlaDataPath["lidar_path"]}/{self.sensor_name}_%.10d.ply' % point_cloud.frame) ))
            return lidar
        elif sensor_type == "Radar":
            radar_bp = self.world.get_blueprint_library().find('sensor.other.radar')
            for key in sensor_options:
                radar_bp.set_attribute(key, sensor_options[key])

            radar = self.world.spawn_actor(radar_bp, transform, attach_to=attached)
            radar.listen(self.save_radar_image)

            return radar
        else:
            return None

    def get_sensor(self):
        return self.sensor

    def save_rgb_image(self, image):
        t_start = self.timer.time()

        image.convert(carla.ColorConverter.Raw)
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]

        if self.display_man.render_enabled():
            self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

    def save_lidar_image(self, image):
        t_start = self.timer.time()
        disp_size = self.display_man.get_display_size()
        lidar_range = 2.0*float(self.sensor_options['range'])

        points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0] / 4), 4))
        lidar_data = np.array(points[:, :2])
        lidar_data *= min(disp_size) / lidar_range
        lidar_data += (0.5 * disp_size[0], 0.5 * disp_size[1])
        lidar_data = np.fabs(lidar_data)  # pylint: disable=E1111
        lidar_data = lidar_data.astype(np.int32)
        lidar_data = np.reshape(lidar_data, (-1, 2))
        lidar_img_size = (disp_size[0], disp_size[1], 3)
        lidar_img = np.zeros((lidar_img_size), dtype=np.uint8)

        lidar_img[tuple(lidar_data.T)] = (255, 255, 255)

        if self.display_man.render_enabled():
            self.surface = pygame.surfarray.make_surface(lidar_img)

        t_end = self.timer.time()
        self.time_processing += (t_end - t_start)
        self.tics_processing += 1



    def save_lidar_image_cv2(self, image):
        t_start = self.timer.time()

        # Display size
        disp_size = self.display_man.get_display_size()
        lidar_range = 2.0 * float(self.sensor_options['range'])

        # Process LiDAR points
        points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0] / 4), 4))

        # Extract (x, y) coordinates
        lidar_data = np.array(points[:, :2])

        # Map coordinates to image display range
        lidar_data *= min(disp_size) / lidar_range
        lidar_data += (0.5 * disp_size[0], 0.5 * disp_size[1])

        # Convert coordinates to integer
        lidar_data = lidar_data.astype(np.int32)
        lidar_data = np.reshape(lidar_data, (-1, 2))

        # Create an empty image (black background)
        lidar_img = np.zeros((disp_size[1], disp_size[0], 3), dtype=np.uint8)

        # Normalize distances for color mapping
        distances = np.linalg.norm(points[:, :2], axis=1)
        norm_distances = distances / np.max(distances)

        # Color mapping based on normalized distances
        color_idxs = np.searchsorted(self.VID_RANGE, norm_distances)
        colors = self.VIDIDIS[np.clip(color_idxs, 0, len(self.VIDIDIS) - 1)] * 255
        colors = colors.astype(np.uint8)
        for i, point in enumerate(lidar_data):
            x, y = point
            if 0 <= x < disp_size[0] and 0 <= y < disp_size[1]:
                lidar_img[y, x] = colors[i]

        # Display the image using OpenCV
        if self.display_man.render_enabled():
            cv2.imshow("LiDAR Image", lidar_img)
            cv2.waitKey(1)

        t_end = self.timer.time()
        self.time_processing += (t_end - t_start)
        self.tics_processing += 1

    def save_semanticlidar_image(self, image):
        t_start = self.timer.time()

        disp_size = self.display_man.get_display_size()
        lidar_range = 2.0*float(self.sensor_options['range'])

        points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0] / 6), 6))
        lidar_data = np.array(points[:, :2])
        lidar_data *= min(disp_size) / lidar_range
        lidar_data += (0.5 * disp_size[0], 0.5 * disp_size[1])
        lidar_data = np.fabs(lidar_data)  # pylint: disable=E1111
        lidar_data = lidar_data.astype(np.int32)
        lidar_data = np.reshape(lidar_data, (-1, 2))
        lidar_img_size = (disp_size[0], disp_size[1], 3)
        lidar_img = np.zeros((lidar_img_size), dtype=np.uint8)

        lidar_img[tuple(lidar_data.T)] = (255, 255, 255)

        if self.display_man.render_enabled():
            self.surface = pygame.surfarray.make_surface(lidar_img)

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

    def save_radar_image(self, radar_data):
        t_start = self.timer.time()
        points = np.frombuffer(radar_data.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (len(radar_data), 4))

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

    def render(self):
        if self.surface is not None:
            offset = self.display_man.get_display_offset(self.display_pos)
            self.display_man.display.blit(self.surface, offset)

    def destroy(self):
        self.sensor.destroy()