import torch
from mmcv.cnn import ConvModule
from mmengine.model import BaseModule
from torch import nn
import torch.nn.functional as F
from BEVFusion.bevfusion import ConvFuser, GeneralizedLSSFPN

def ConvFuser_input_output():

    # 创建输入张量，假设每个张量的形状为 (batch_size, channels, height, width)
    batch_size = 1
    height = 2
    width = 2

    # 假设有3个输入张量，每个输入张量的通道数不同
    input1 = torch.randn(batch_size, 3, height, width)  # (2, 3, 5, 5)
    input2 = torch.randn(batch_size, 5, height, width)  # (2, 5, 5, 5)
    input3 = torch.randn(batch_size, 2, height, width)  # (2, 2, 5, 5)

    # 创建 ConvFuser 模块实例，输入的通道数是 [3, 5, 2]，输出的通道数是 4
    conv_fuser = ConvFuser(in_channels=[3, 5, 2], out_channels=4)

    # 前向传播，输入是一个张量列表
    inputs = [input1, input2, input3]
    output = conv_fuser(inputs)

    # 输出结果
    print("Output shape:", output.shape)

def GeneralizedLSSFPN_TEST():
    # 输入特征图
    inputs = [
        torch.randn(1, 64, 32, 32),  # 64 channels
        torch.randn(1, 128, 16, 16),  # 128 channels
        torch.randn(1, 256, 8, 8),  # 256 channels
        torch.randn(1, 512, 4, 4)  # 512 channels
    ]

    # 实例化 GeneralizedLSSFPN
    img_neck = GeneralizedLSSFPN(
        in_channels=[64, 128, 256, 512],
        out_channels=256,
        start_level=0,
        num_outs=3,
        norm_cfg=dict(type='BN2d', requires_grad=True),
        act_cfg=dict(type='ReLU', inplace=True),
        upsample_cfg=dict(mode='bilinear', align_corners=False))

    # 前向传播
    outputs = img_neck(inputs)

    # 打印输出形状
    for i, output in enumerate(outputs):
        print(f"Output {i + 1} shape: {output.shape}")
if __name__ == '__main__':
    # ConvFuser_input_output()
    GeneralizedLSSFPN_TEST()
