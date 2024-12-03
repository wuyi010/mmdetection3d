import carla
import cv2
import numpy as np
import pygame

from carla_project.carla_simu import CustomTimer


# SensorManager(world, display_manager, 'RGBCamera', carla_project.Transform(carla_project.Location(x=0, z=2.4), carla_project.Rotation(yaw=-90)), vehicle, {}, display_pos=[0, 0])
class SensorManager:
    def __init__(self, world, display_man, sensor_type, transform, attached, sensor_options, display_pos, sensor_name, args):
        self.sensor_name = sensor_name
        self.args = args
        self.surface = None
        self.world = world
        self.display_man = display_man
        self.display_pos = display_pos
        self.sensor = self.init_sensor(sensor_type, transform, attached, sensor_options, sensor_name, args)
        self.sensor_options = sensor_options
        self.timer = CustomTimer()
        self.point_cloud_data = []  # 存储接收到的点云数据
        self.frame_collected = 0  # 用于统计收集到的雷达帧数


        self.time_processing = 0.0
        self.tics_processing = 0

        self.display_man.add_sensor(self)

        # # Create colormap (plasma in this case)
        # self.VIDIDIS = np.array(cm.get_cmap("plasma").colors)
        # self.VID_RANGE = np.linspace(0.0, 1.0, self.VIDIDIS.shape[0])
        #
        # self.image_queue = queue.Queue()  # 创建图像队列
        # self.stop_event = threading.Event()  # 用于停止线程

        # # 启动保存图像的线程
        # self.saving_thread = threading.Thread(target=self.save_images)
        # self.saving_thread.start()

    def init_sensor(self, sensor_type, transform, attached, sensor_options,sensor_name,args):
        if sensor_type == 'RGBCamera':
            camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')

            disp_size = self.display_man.get_display_size()
            camera_bp.set_attribute('image_size_x', str(disp_size[0]))
            camera_bp.set_attribute('image_size_y', str(disp_size[1]))

            for key in sensor_options:
                camera_bp.set_attribute(key, sensor_options[key])

            camera = self.world.spawn_actor(camera_bp, transform, attach_to=attached)
            camera.listen(lambda image:(
                self.save_rgb_image(image), # 调用原来的保存函数
                image.save_to_disk(f'{self.args.save_path}/{self.args.camera_path}/%.6d-C{self.sensor_name}.png' % image.frame)))# 保存图像到磁盘
            return camera

        elif sensor_type == 'LiDAR':
            lidar_bp = self.world.get_blueprint_library().find('sensor.lidar.ray_cast')

            lidar_bp.set_attribute('range', '100')
            lidar_bp.set_attribute('dropoff_general_rate', lidar_bp.get_attribute('dropoff_general_rate').recommended_values[0])
            lidar_bp.set_attribute('dropoff_intensity_limit', lidar_bp.get_attribute('dropoff_intensity_limit').recommended_values[0])
            lidar_bp.set_attribute('dropoff_zero_intensity', lidar_bp.get_attribute('dropoff_zero_intensity').recommended_values[0])

            for key in sensor_options:
                lidar_bp.set_attribute(key, sensor_options[key])

            lidar = self.world.spawn_actor(lidar_bp, transform, attach_to=attached)
            lidar.listen(lambda point_cloud:(
                self.save_lidar_image(point_cloud),
                point_cloud.save_to_disk(f'{args.save_path}/{args.lidar_path}/%.6d-L{sensor_name}.ply' % point_cloud.frame) ))
            return lidar

        elif sensor_type == 'SemanticLiDAR':
            lidar_bp = self.world.get_blueprint_library().find('sensor.lidar.ray_cast_semantic')
            lidar_bp.set_attribute('range', '100')

            for key in sensor_options:
                lidar_bp.set_attribute(key, sensor_options[key])

            lidar = self.world.spawn_actor(lidar_bp, transform, attach_to=attached)

            lidar.listen(self.save_semanticlidar_image)

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