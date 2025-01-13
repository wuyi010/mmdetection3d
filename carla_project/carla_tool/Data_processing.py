import os
from PIL import Image


def crop_image_to_size(image_input,  target_width, target_height,output_image_path=None,):
    """
    按中心裁剪图像为指定尺寸 (target_width, target_height)

    参数:
    - image_input: 输入图像，可以是图像路径 (str) 或 PIL.Image.Image 对象
    - output_image_path: 裁剪后图像的保存路径，如果不需要保存，可以为 None
    - target_width: 裁剪后的图像宽度，如果不需要调整宽度，可以为 None
    - target_height: 裁剪后的图像高度，如果不需要调整高度，可以为 None
    """
    # 如果 input_image 是字符串，则认为是路径，打开图像
    if isinstance(image_input, str):
        img = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        raise TypeError("input_image 必须是图像路径 (str) 或 PIL.Image.Image 对象")

    # 获取图像的宽度和高度
    width, height = img.size

    # 确保提供了目标尺寸，并且目标尺寸不超过原始图像尺寸
    if target_width is None or target_height is None:
        raise ValueError("必须提供 target_width 和 target_height")
    if target_width > width or target_height > height:
        raise ValueError("目标尺寸不能大于原图像尺寸")

    # 计算中心裁剪的边界
    left = (width - target_width) / 2
    top = (height - target_height) / 2
    right = (width + target_width) / 2
    bottom = (height + target_height) / 2

    # 裁剪图像
    cropped_img = img.crop((left, top, right, bottom))

    # 如果提供了保存路径，则保存裁剪后的图像
    if output_image_path:
        cropped_img.save(output_image_path)
        print(f"裁剪后的图像已保存至: {output_image_path}")

    return cropped_img


from PIL import Image
import os

from PIL import Image

def resize_images(image_input, output_paths=None, target_size=(1600, 900)):
    """
    Args:
    - image_input: 输入图像的路径或PIL图像对象，可以是单个字符串、单个图像对象或它们的列表。
    - output_paths: 输出图像的路径，默认为与输入路径相同，如果输入是图像对象则为None。
    - target_size: 调整后的目标尺寸，默认为 (1600, 900)。
    """
    # 如果没有提供输出路径并且输入是路径，设置输出路径为输入路径
    if output_paths is None:
        output_paths = image_input

    # 将单个字符串或图像对象转换为列表
    if isinstance(image_input, (str, Image.Image)):
        image_paths = [image_input]
    if isinstance(output_paths, str):
        output_paths = [output_paths]

    # 遍历每个图像进行大小调整
    resized_images = []  # 如果需要返回调整后的图像对象
    for i, image_path in enumerate(image_paths):
        # 如果输入是路径，打开图像
        if isinstance(image_path, str):
            img = Image.open(image_path)
        elif isinstance(image_path, Image.Image):
            img = image_path
        else:
            raise ValueError("输入必须是图像路径或PIL图像对象")

        # 调整图像大小
        resized_img = img.resize(target_size, Image.LANCZOS)

        # 如果输出路径是路径，保存调整后的图像
        if output_paths and isinstance(output_paths, list) and isinstance(output_paths[i], str):
            output_path = output_paths[i]
            resized_img.save(output_path)
            print(f"Image resized and saved to {output_path}")
        else:
            # 如果没有提供输出路径或输出路径为None，添加到结果列表
            resized_images.append(resized_img)

    # 如果未指定输出路径，则返回调整后的图像对象
    if not isinstance(output_paths, list):
        return resized_images if len(resized_images) > 1 else resized_images[0]

def generate_white_image(width, height, output_path=None):
    """
    生成一个指定大小的纯白图像（像素全为255）。

    Args:
    - width: 图像宽度（像素）
    - height: 图像高度（像素）
    - output_path: 如果指定了路径，则保存图像到该路径，否则返回图像对象。

    Returns:
    - 如果没有提供 output_path，返回生成的PIL图像对象。
    """
    # 创建一个指定大小的纯白图像（像素值为255）
    white_image = Image.new('RGB', (width, height), color=(255, 255, 255))

    # 如果指定了输出路径，保存图像
    if output_path:
        white_image.save(output_path)
        print(f"Image saved to {output_path}")
    else:
        return white_image

def resize_and_combine_images_Lateral_by_height(image_input, output_path, target_height=900):
    """
      输入一组图像路径或图像对象，并将这些图像裁剪为指定高度，按顺序横向拼接。

      参数:
      - image_input: 需要处理的图像路径或图像对象列表
      - output_path: 合并后图像的保存路径，默认为None，仅返回合并图像对象
      - target_height: 需要裁剪的目标高度，默认为900
      """
    # 打开所有图像并根据目标高度调整尺寸，保持宽高比
    images = []
    for input_item in image_input:
        if isinstance(input_item, str):
            # 如果是路径，打开图像
            img = Image.open(input_item)
        else:
            # 如果是图像对象，直接使用
            img = input_item

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

    # 如果提供了输出路径，保存合并后的图像
    if output_path:
        combined_image.save(output_path)
        print(f"合并后的图像已保存至: {output_path}")

    return combined_image


from PIL import Image


from PIL import Image

def resize_and_combine_images_vertical_by_width(image_inputs, output_path=None, target_width=1600):
    """
    输入一组图像路径或图像对象，并将这些图像裁剪为指定宽度，按顺序垂直拼接。

    参数:
    - image_inputs: 需要处理的图像路径或图像对象列表
    - output_path: 合并后图像的保存路径，默认为None，仅返回合并图像对象
    - target_width: 需要裁剪的目标宽度，默认为1600
    """
    # 打开所有图像并根据目标宽度调整尺寸，保持宽高比
    images = []
    for input_item in image_inputs:
        if isinstance(input_item, list):  # 如果元素是列表，递归处理
            images.extend(resize_and_combine_images_vertical_by_width(input_item, target_width=target_width))  # 递归调用处理列表中的图像
        else:
            if isinstance(input_item, str):
                # 如果是路径，打开图像
                img = Image.open(input_item)
            else:
                # 如果是图像对象，直接使用
                img = input_item

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

    # 如果提供了输出路径，保存合并后的图像
    if output_path:
        combined_image.save(output_path)
        print(f"合并后的图像已保存至: {output_path}")

    return combined_image



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

