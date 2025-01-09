import os
from PIL import Image


def crop_image_to_size(input_image_path, output_image_path, target_width, target_height):
    """
    按中心裁剪图像为指定尺寸 (target_width, target_height)

    参数:
    - input_image_path: 输入图像的路径
    - output_image_path: 裁剪后图像的保存路径
    - target_width: 裁剪后的图像宽度
    - target_height: 裁剪后的图像高度
    """
    # 打开图像
    with Image.open(input_image_path) as img:
        # 获取图像的宽度和高度
        width, height = img.size

        # 确保目标尺寸不超过原始图像尺寸
        if target_width > width or target_height > height:
            raise ValueError("目标尺寸不能大于原图像尺寸")

        # 计算中心裁剪的边界
        left = (width - target_width) / 2
        top = (height - target_height) / 2
        right = (width + target_width) / 2
        bottom = (height + target_height) / 2

        # 裁剪图像
        cropped_img = img.crop((left, top, right, bottom))

        # 保存裁剪后的图像
        cropped_img.save(output_image_path)
        print(f"裁剪后的图像已保存至: {output_image_path}")


from PIL import Image
import os


def resize_images(image_paths, output_paths=None, target_size=(1600, 900)):
    """
    Args:
    image_paths: 输入图像的路径，可以是单个字符串或字符串列表。
    output_paths: 输出图像的路径，默认为 image_paths。
    target_size: 调整后的目标尺寸，默认为 (1600, 900)。
    """
    # 如果没有提供输出路径，则输出路径和输入路径相同
    if output_paths is None:
        output_paths = image_paths

    # 如果输入是单个字符串，而不是列表，将其转换为列表
    if isinstance(image_paths, str):
        image_paths = [image_paths]
    if isinstance(output_paths, str):
        output_paths = [output_paths]

    # 遍历每个图像进行大小调整
    for i, image_path in enumerate(image_paths):
        # 打开图像
        with Image.open(image_path) as img:
            # 调整图像大小
            resized_img = img.resize(target_size, Image.LANCZOS)

            # 保存调整后的图像，输出路径与输入图像相同，或者按用户指定的路径保存
            output_path = output_paths[i] if output_paths else image_path
            resized_img.save(output_path)
            print(f"Image resized and saved to {output_path}")


def resize_and_combine_images_Lateral_by_height(image_paths, output_path, target_height=900):
    """
    输入一组图像路径，并将这些图像裁剪为指定高度，按顺序横向拼接保存到指定路径。

    参数:
    - image_paths: 需要处理的图像路径列表
    - output_path: 合并后图像的保存路径
    - target_height: 需要裁剪的目标高度，默认为900
    """
    # 打开所有图像并根据目标高度调整尺寸，保持宽高比
    images = []
    for path in image_paths:
        img = Image.open(path)
        width, height = img.size
        new_width = int(width * target_height / height)  # 根据高度调整宽度，保持宽高比
        resized_img = img.resize((new_width, target_height))
        images.append(resized_img)

    # 确保所有图像的高度一致（通过调整尺寸来确保）
    height = target_height
    total_width = sum(img.size[0] for img in images)  # 总宽度是所有图像宽度之和

    # 创建一个新的空白图像，宽度是n张图像的宽度之和，高度保持目标高度
    combined_image = Image.new('RGB', (total_width, height))

    # 依次粘贴每张图像
    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.size[0]  # 根据图像的宽度更新偏移量

    # 保存合并后的图像
    combined_image.save(output_path)
    print(f"合并后的图像已保存至: {output_path}")

def resize_and_combine_images_vertical_by_width(image_paths, output_path, target_width=1600):
    """
    输入一组图像路径，并将这些图像裁剪为指定宽度，按顺序垂直拼接保存到指定路径。

    参数:
    - image_paths: 需要处理的图像路径列表
    - output_path: 合并后图像的保存路径
    - target_width: 需要裁剪的目标宽度，默认为1600
    """
    # 打开所有图像并根据目标宽度调整尺寸，保持宽高比
    images = []
    for path in image_paths:
        img = Image.open(path)
        width, height = img.size
        new_height = int(height * target_width / width)  # 根据宽度调整高度，保持宽高比
        resized_img = img.resize((target_width, new_height))
        images.append(resized_img)

    # 确保所有图像的宽度一致（通过调整尺寸来确保）
    width = target_width
    total_height = sum(img.size[1] for img in images)  # 总高度是所有图像高度之和

    # 创建一个新的空白图像，宽度保持目标宽度，高度是所有图像高度之和
    combined_image = Image.new('RGB', (width, total_height))

    # 依次粘贴每张图像
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.size[1]  # 根据图像的高度更新偏移量

    # 保存合并后的图像
    combined_image.save(output_path)
    print(f"合并后的图像已保存至: {output_path}")

def split_image(image_path, output_dir):
    """
    将图像裁剪为6个部分并保存到指定目录中。

    参数:
    - image_path: 原图像的路径
    - output_dir: 裁剪后图像的保存目录
    """
    # 打开原图像
    image = Image.open(image_path)

    # 图像的原始尺寸
    img_width, img_height = image.size
    print(f"原图像大小: {img_width}x{img_height}")

    # 计算每个子图像的宽度和高度
    sub_img_width = img_width // 3  # 每列的宽度
    sub_img_height = img_height // 2  # 每行的高度

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 依次裁剪出6个部分并保存
    for row in range(2):  # 两行
        for col in range(3):  # 三列
            left = col * sub_img_width
            upper = row * sub_img_height
            right = left + sub_img_width
            lower = upper + sub_img_height
            cropped_img = image.crop((left, upper, right, lower))

            # 生成文件名，保存分割后的图像
            output_path = os.path.join(output_dir, f"{row * 3 + col + 1}.png")
            cropped_img.save(output_path)
            print(f"保存: {output_path}")

