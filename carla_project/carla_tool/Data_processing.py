import os

import numpy as np
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
from PIL import Image
from PIL import Image


def resize_images(image_input, output_paths=None, target_size=(1600, 900)):
    """
    将输入图像调整到指定大小，并返回处理后的图像对象。

    Args:
    - image_input: 输入图像的路径或PIL图像对象，可以是单个字符串、单个图像对象或它们的列表。
    - output_paths: 输出图像的路径，可选。如果指定则保存调整后的图像。
    - target_size: 调整后的目标尺寸，默认为 (1600, 900)。

    Returns:
    - 返回调整后的图像对象，如果输入为多个图像，返回图像对象列表。
    """
    # 如果输入是单个字符串或图像对象，转换为列表
    if isinstance(image_input, (str, Image.Image)):
        image_input = [image_input]
    if isinstance(output_paths, str):
        output_paths = [output_paths]

    # 用于存储调整后的图像对象
    resized_images = []

    # 遍历每个图像并调整大小
    for i, image_path in enumerate(image_input):
        # 如果输入是路径，打开图像
        if isinstance(image_path, str):
            img = Image.open(image_path)
        elif isinstance(image_path, Image.Image):
            img = image_path
        else:
            raise ValueError("输入必须是图像路径或PIL图像对象")

        # 调整图像大小
        resized_img = img.resize(target_size, Image.LANCZOS)
        resized_images.append(resized_img)

        # 如果指定了输出路径，保存调整后的图像
        if output_paths and isinstance(output_paths[i], str):
            resized_img.save(output_paths[i])
            print(f"Image resized and saved to {output_paths[i]}")

    # 如果只有一个图像，返回该图像对象；否则返回图像对象列表
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

    return white_image
from PIL import Image

def generate_black_image(width, height, output_path=None):
    """
    生成一个指定大小的纯黑图像（像素全为0）。

    Args:
    - width: 图像宽度（像素）
    - height: 图像高度（像素）
    - output_path: 如果指定了路径，则保存图像到该路径，否则返回图像对象。

    Returns:
    - 如果没有提供 output_path，返回生成的PIL图像对象。
    """
    # 创建一个指定大小的纯黑图像（像素值为0）
    black_image = Image.new('RGB', (width, height), color=(0, 0, 0))

    # 如果指定了输出路径，保存图像
    if output_path:
        black_image.save(output_path)
        print(f"Image saved to {output_path}")

    return black_image

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
            try:
                img = Image.open(input_item)
            except Exception as e:
                print(f"无法打开图像: {input_item}, 错误: {e}")
                continue  # 跳过无法加载的图像
        else:
            # 如果是图像对象，直接使用
            img = input_item

        if img is None:
            print(f"图像加载失败，跳过: {input_item}")
            continue

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

from PIL import Image


def resize_and_combine_images_vertical_by_width(image_inputs, output_path=None, target_width=1600):
    """
    输入一组图像路径或图像对象列表，并将这些图像裁剪为指定宽度，按顺序垂直拼接。

    参数:
    - image_inputs: 需要处理的图像路径或图像对象列表
    - output_path: 合并后图像的保存路径，默认为None，如果为None，返回最终的合并图像对象，如果提供了路径，将对象保存到该路径，并返回该对象
    - target_width: 需要裁剪的目标宽度，默认为1600

    返回:
    - 最终的合并图像对象
    """
    # 打开所有图像并根据目标宽度调整尺寸，保持宽高比
    images = []
    for input_item in image_inputs:
        if isinstance(input_item, str):
            # 如果是路径，打开图像
            img = Image.open(input_item)
        else:
            # 如果是图像对象，直接使用
            img = input_item

        # if img is None:
        #     raise ValueError(f"无法读取图像：{input_item}")

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

    # 返回合并后的图像
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



import cv2


def draw_rectangles_on_image(image_input, rectangles,output_path=None,):
    """
    在图像上绘制多个矩形框。

    参数:
    - image_input: str 或者 图像对象, 可以是图像路径，也可以是已读取的图像对象。
    - rectangles: list, 每个矩形框的参数字典，包括起始点、结束点、颜色和厚度。

    返回:
    - image_with_rectangles: 绘制了矩形框的图像对象（PIL.Image.Image类型）。
    """
    # 如果输入是 PIL.Image.Image 类型，则先转换为 NumPy 数组
    if isinstance(image_input, Image.Image):
        image = np.array(image_input)
    elif isinstance(image_input, str):
        image = cv2.imread(image_input)
        if image is None:
            raise ValueError(f"Failed to load image from path: {image_input}")
    else:
        raise ValueError("Invalid image input type")

    # 在图像上绘制多个矩形框
    for rect in rectangles:
        image = cv2.rectangle(
            image,
            rect['start_point'],
            rect['end_point'],
            rect['color'],
            rect['thickness']
        )

    # 将修改后的图像转换回 PIL.Image.Image 类型
    image_with_rectangles = Image.fromarray(image)
    # 如果指定了 output_path，则保存图像
    if output_path:
        image_with_rectangles.save(output_path)
    # 返回带有矩形框的图像对象
    return image_with_rectangles


from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2


def draw_shapes_and_write_numbers_on_image(image_input, shapes, numbers, output_path=None):
    """
    在图像上绘制图形（如矩形、圆形等）并在指定位置写数字。

    参数:
    - image_input: str 或者 图像对象, 可以是图像路径，也可以是已读取的图像对象。
    - shapes: list, 每个图形的参数字典，包括形状类型（矩形或圆形）、位置、大小、颜色和厚度。
    - numbers: list, 每个数字的参数字典，包括位置、数字内容和颜色。

    返回:
    - image_with_shapes_and_numbers: 绘制了图形和数字的图像对象（PIL.Image.Image类型）。
    """
    # 如果输入是 PIL.Image.Image 类型，则先转换为 NumPy 数组
    if isinstance(image_input, Image.Image):
        image = np.array(image_input)
    elif isinstance(image_input, str):
        image = cv2.imread(image_input)
        if image is None:
            raise ValueError(f"Failed to load image from path: {image_input}")
    else:
        raise ValueError("Invalid image input type")

    # 将图像从 BGR 转换为 RGB，因为 PIL 使用 RGB 格式
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)

    # 创建一个ImageDraw对象以便在图像上绘制
    draw = ImageDraw.Draw(pil_image)

    # 设置字体（调整为更大的字体）
    try:
        font = ImageFont.truetype("arial.ttf", 60)  # 设置字体大小为 60
    except IOError:
        font = ImageFont.load_default()  # 使用默认字体

    # 绘制图形（矩形、圆形等）
    for shape in shapes:
        shape_type = shape['type']
        if shape_type == 'rectangle':
            # 矩形框
            start_point = shape['start_point']
            end_point = shape['end_point']
            color = shape['color']
            thickness = shape['thickness']
            image = cv2.rectangle(image, start_point, end_point, color, thickness)
        elif shape_type == 'circle':
            # 圆形
            center = shape['center']
            radius = shape['radius']
            color = shape['color']
            thickness = shape['thickness']
            image = cv2.circle(image, center, radius, color, thickness)

    # 在图像上写数字
    for number in numbers:
        position = number['position']
        text = str(number['value'])
        color = number['color']

        # 获取文本的大小并调整位置使其居中
        text_width, text_height = draw.textsize(text, font=font)
        text_position = (position[0] - text_width // 2, position[1] - text_height // 2)

        # 绘制数字
        draw.text(text_position, text, fill=color, font=font)

    # 将修改后的图像转换回 PIL.Image.Image 类型，并转回 BGR 格式保存
    image_with_shapes_and_numbers = np.array(pil_image)
    image_with_shapes_and_numbers = cv2.cvtColor(image_with_shapes_and_numbers, cv2.COLOR_RGB2BGR)

    # 如果指定了 output_path，则保存图像
    if output_path:
        cv2.imwrite(output_path, image_with_shapes_and_numbers)

    # 返回带有图形和数字的图像对象
    return image_with_shapes_and_numbers

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def draw_circle_and_number_with_matplotlib(image_input, circle_position, circle_radius, number, number_position, circle_color=(0, 0, 255), number_color=(0, 0, 0), output_path=None):
    """
    在图像上绘制圆形，并在指定位置使用matplotlib格式绘制数字。

    参数:
    - image_input: PIL 图像对象。
    - circle_position: 圆心位置，格式为 (x, y)。
    - circle_radius: 圆形半径。
    - number: 要显示的数字。
    - number_position: 数字的位置，格式为 (x, y)。
    - circle_color: 圆形的颜色（默认蓝色）。
    - number_color: 数字的颜色（默认黑色）。
    - output_path: 可选，保存图像的路径。

    返回:
    - image_with_circle_and_number: 绘制了圆形和数字的图像对象。
    """
    # 如果输入是 PIL.Image.Image 类型，则直接使用
    if isinstance(image_input, Image.Image):
        image = image_input.copy()
    else:
        raise ValueError("Invalid image input type")

    # 创建一个ImageDraw对象以便在图像上绘制
    draw = ImageDraw.Draw(image)

    # 绘制圆形
    draw.ellipse(
        [circle_position[0] - circle_radius, circle_position[1] - circle_radius,
         circle_position[0] + circle_radius, circle_position[1] + circle_radius],
        outline=circle_color, width=5  # 圆形边框的宽度为5
    )

    # 使用 matplotlib 的 plt.text 绘制数字
    fig, ax = plt.subplots()  # 创建一个matplotlib图形
    ax.imshow(np.array(image))  # 显示图片
    ax.text(
        number_position[0], number_position[1], str(number),
        fontsize=2, color=number_color, ha='left', va='center', fontname='Arial'
    )

    # 获取带有数字的图像
    plt.axis('off')  # 不显示坐标轴
    fig.canvas.draw()

    # 将matplotlib图形转换为 PIL 图像
    image_with_number = np.array(fig.canvas.renderer.buffer_rgba())
    image_with_number = Image.fromarray(image_with_number)

    # 返回带有圆形和数字的图像对象
    if output_path:
        image_with_number.save(output_path)

    return image_with_number


