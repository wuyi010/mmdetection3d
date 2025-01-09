#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
CARLA Dynamic Weather:

Connect to a CARLA Simulator instance and control the weather. Change Sun
position smoothly with time and generate storms occasionally.
"""

import glob
import os
import sys

import carla

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import argparse
import math


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(value, maximum))


class Sun(object):
    def __init__(self, azimuth, altitude):
        self.azimuth = azimuth
        self.altitude = altitude
        self._t = 0.0

    def tick(self, delta_seconds):
        self._t += 0.008 * delta_seconds
        self._t %= 2.0 * math.pi
        self.azimuth += 0.25 * delta_seconds
        self.azimuth %= 360.0
        self.altitude = (70 * math.sin(self._t)) - 20

    def __str__(self):
        return 'Sun(alt: %.2f, azm: %.2f)' % (self.altitude, self.azimuth)


class Storm(object):
    def __init__(self, precipitation):
        self._t = precipitation if precipitation > 0.0 else -50.0
        self._increasing = True
        self.clouds = 0.0
        self.rain = 0.0
        self.wetness = 0.0
        self.puddles = 0.0
        self.wind = 0.0
        self.fog = 0.0

    def tick(self, delta_seconds):
        delta = (1.3 if self._increasing else -1.3) * delta_seconds
        self._t = clamp(delta + self._t, -250.0, 100.0)
        self.clouds = clamp(self._t + 40.0, 0.0, 90.0)
        self.rain = clamp(self._t, 0.0, 80.0)
        delay = -10.0 if self._increasing else 90.0
        self.puddles = clamp(self._t + delay, 0.0, 85.0)
        self.wetness = clamp(self._t * 5, 0.0, 100.0)
        self.wind = 5.0 if self.clouds <= 20 else 90 if self.clouds >= 70 else 40
        self.fog = clamp(self._t - 10, 0.0, 30.0)
        if self._t == -250.0:
            self._increasing = True
        if self._t == 100.0:
            self._increasing = False

    def __str__(self):
        return 'Storm(clouds=%d%%, rain=%d%%, wind=%d%%)' % (self.clouds, self.rain, self.wind)


class Weather(object):
    def __init__(self, weather):
        self.weather = weather
        self._sun = Sun(weather.sun_azimuth_angle, weather.sun_altitude_angle)
        self._storm = Storm(weather.precipitation)

    def tick(self, delta_seconds):
        self._sun.tick(delta_seconds)
        self._storm.tick(delta_seconds)
        self.weather.cloudiness = self._storm.clouds
        self.weather.precipitation = self._storm.rain
        self.weather.precipitation_deposits = self._storm.puddles
        self.weather.wind_intensity = self._storm.wind
        self.weather.fog_density = self._storm.fog
        self.weather.wetness = self._storm.wetness
        self.weather.sun_azimuth_angle = self._sun.azimuth
        self.weather.sun_altitude_angle = self._sun.altitude

    def __str__(self):
        return '%s %s' % (self._sun, self._storm)

def set_custom_weather(world):
    custom_weather = carla.WeatherParameters(
        cloudiness=20.0,  # 云量 80%
        precipitation=0.0,  # 降雨量 50%
        precipitation_deposits=1.0,  # 地面湿度
        wind_intensity=20.0,  # 风力强度
        fog_density=0.1,  # 雾浓度
        sun_azimuth_angle=0.0,  # 太阳方位角
        sun_altitude_angle=20.0  # 太阳高度角
    )
    world.set_weather(custom_weather)

def set_rain_snow_weather(world):
    custom_weather = carla.WeatherParameters(
        cloudiness=50,  # 云量 90%
        precipitation=90.0,  # 降水量 80%（表示大雨或大雪）
        precipitation_deposits=100.0,  # 地面湿度 100%（积水或积雪）
        wind_intensity=50.0,  # 风力强度 50%
        fog_density=8.0,  # 雾浓度 30%（雨雪天气经常伴随雾气）
        wetness=90.0,  # 地面湿滑度，雨雪时较高
        # snow=True,  # 设置为 True 模拟降雪（在某些 CARLA 版本中有此选项）
        sun_azimuth_angle=45.0,  # 太阳方位角
        sun_altitude_angle=5.0  # 太阳高度角（降低太阳高度以模拟更阴暗的天气）
    )
    world.set_weather(custom_weather)


def set_rain_fog_weather(world):
    custom_weather = carla.WeatherParameters(
        cloudiness=50,  # 云量 90%
        precipitation=90.0,  # 降水量 80%（表示大雨或大雪）
        precipitation_deposits=90.0,  # 地面湿度 100%（积水或积雪）
        wind_intensity=50.0,  # 风力强度 50%
        fog_density=85.0,  # 雾浓度 30%（雨雪天气经常伴随雾气）
        wetness=90.0,  # 地面湿滑度，雨雪时较高
        # snow=True,  # 设置为 True 模拟降雪（在某些 CARLA 版本中有此选项）
        sun_azimuth_angle=45.0,  # 太阳方位角
        sun_altitude_angle=5.0  # 太阳高度角（降低太阳高度以模拟更阴暗的天气）
    )
    world.set_weather(custom_weather)
def set_night_rain_snow_weather(world):
    custom_weather = carla.WeatherParameters(
        cloudiness=50,  # 云量 50%
        precipitation=90.0,  # 降水量 90%（大雨或大雪）
        precipitation_deposits=100.0,  # 地面湿度 100%
        wind_intensity=50.0,  # 风力强度 50%
        fog_density=30.0,  # 雾浓度 50%
        wetness=90.0,  # 地面湿滑度
        sun_azimuth_angle=45.0,  # 太阳方位角
        sun_altitude_angle=-10.0  # 太阳高度角为负值，模拟夜晚
    )
    world.set_weather(custom_weather)


def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-s', '--speed',
        metavar='FACTOR',
        default=1,
        type=float,
        help='rate at which the weather changes (default: 1.0)')
    args = argparser.parse_args()

    speed_factor = args.speed
    update_freq = 0.1 / speed_factor

    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)
    world = client.get_world()

    weather = Weather(world.get_weather())

    elapsed_time = 0.0
    set_custom_weather(world)
    while True:
        timestamp = world.wait_for_tick(seconds=30.0).timestamp
        elapsed_time += timestamp.delta_seconds
        if elapsed_time > update_freq:
            weather.tick(speed_factor * elapsed_time)
            world.set_weather(weather.weather)
            # set_custom_weather(world)
            sys.stdout.write('\r' + str(weather) + 12 * ' ')
            sys.stdout.flush()
            elapsed_time = 0.0


if __name__ == '__main__':

    main()
