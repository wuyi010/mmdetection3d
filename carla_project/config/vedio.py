from moviepy.editor import VideoFileClip


def video_to_gif(video_path, gif_path, start_time=0, duration=None, fps=10):
    """
    将视频转换为动态图（GIF）。

    参数：
    - video_path: 输入视频文件路径。
    - gif_path: 输出GIF文件路径。
    - start_time: 视频开始转换的时间（秒），默认从0秒开始。
    - duration: 转换的时长（秒），默认转换到视频末尾。
    - fps: GIF的帧率，默认10帧每秒。
    """
    # 载入视频
    clip = VideoFileClip(video_path).subclip(start_time, start_time + duration if duration else None)

    # 写入GIF文件
    clip.write_gif(gif_path, fps=fps)

    print(f"GIF生成成功：{gif_path}")


if __name__ == "__main__":
    # 示例：将当前目录下的 input_video.mp4 制作为 output.gif，取前10秒，帧率10fps
    video_to_gif("input_video.mp4", "/home/didi/mmdetection3d_ing/carla_project/config/output.gif", start_time=15, duration=16, fps=10)
