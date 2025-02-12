# Copyright (c) OpenMMLab. All rights reserved.
import warnings
from typing import Optional, Sequence, Tuple

import torch
from mmcv.cnn import build_conv_layer, build_norm_layer
from mmengine.model import BaseModule
from torch import Tensor
from torch import nn as nn

from mmdet3d.registry import MODELS
from mmdet3d.utils import ConfigType, OptMultiConfig


@MODELS.register_module()
class SECOND(BaseModule):
    """Backbone network for SECOND/PointPillars/PartA2/MVXNet.

    Args:
        in_channels (int): Input channels.
        out_channels (list[int]): Output channels for multi-scale feature maps.
        layer_nums (list[int]): Number of layers in each stage.
        layer_strides (list[int]): Strides of each stage.
        norm_cfg (dict): Config dict of normalization layers.
        conv_cfg (dict): Config dict of convolutional layers.
    """

    def __init__(self,
                 in_channels: int = 128,
                 out_channels: Sequence[int] = [128, 128, 256],
                 layer_nums: Sequence[int] = [3, 5, 5],
                 layer_strides: Sequence[int] = [2, 2, 2],
                 norm_cfg: ConfigType = dict(
                     type='BN', eps=1e-3, momentum=0.01),
                 conv_cfg: ConfigType = dict(type='Conv2d', bias=False),
                 init_cfg: OptMultiConfig = None,
                 pretrained: Optional[str] = None) -> None:
        super(SECOND, self).__init__(init_cfg=init_cfg)
        assert len(layer_strides) == len(layer_nums)
        assert len(out_channels) == len(layer_nums)

        in_filters = [in_channels, *out_channels[:-1]]
        # note that when stride > 1, conv2d with same padding isn't
        # equal to pad-conv2d. we should use pad-conv2d.
        blocks = []
        for i, layer_num in enumerate(layer_nums):
            block = [
                build_conv_layer(
                    conv_cfg,
                    in_filters[i],
                    out_channels[i],
                    3,
                    stride=layer_strides[i],
                    padding=1),
                build_norm_layer(norm_cfg, out_channels[i])[1],
                nn.ReLU(inplace=True),
            ]
            for j in range(layer_num):
                block.append(
                    build_conv_layer(
                        conv_cfg,
                        out_channels[i],
                        out_channels[i],
                        3,
                        padding=1))
                block.append(build_norm_layer(norm_cfg, out_channels[i])[1])
                block.append(nn.ReLU(inplace=True))

            block = nn.Sequential(*block)
            blocks.append(block)

        self.blocks = nn.ModuleList(blocks)

        assert not (init_cfg and pretrained), \
            'init_cfg and pretrained cannot be setting at the same time'
        if isinstance(pretrained, str):
            warnings.warn('DeprecationWarning: pretrained is a deprecated, '
                          'please use "init_cfg" instead')
            self.init_cfg = dict(type='Pretrained', checkpoint=pretrained)
        else:
            self.init_cfg = dict(type='Kaiming', layer='Conv2d')

    def forward(self, x: Tensor) -> Tuple[Tensor, ...]:
        """Forward function.

        Args:
            x (torch.Tensor): Input with shape (N, C, H, W).

        Returns:
            tuple[torch.Tensor]: Multi-scale features.
        """
        outs = []
        for i in range(len(self.blocks)):
            x = self.blocks[i](x)
            outs.append(x)
        return tuple(outs)



# model = SECOND(
#     in_channels=256,         # 输入通道数
#     layer_nums=[5, 5],       # 每个块的卷积层数量
#     layer_strides=[1, 2],    # 每个块的第一个卷积层的步幅
#     out_channels=[128, 256]  # 每个块的输出通道数
# )
#
#
# # Instantiate model and forward pass
# # Simulating input tensor of shape (N, C, H, W) where N=1 (batch size), C=128 (input channels), H=256, W=256
# input_tensor = torch.randn(1, 256, 256, 256)
#
#
#
# output = model(input_tensor)
#
# # Display the model structure and the output shape for each layer
#
# output_shapes = [out.shape for out in output]
#
# print( "model：",model,)
# # Loop through the tuple and print the shape of each output tensor
# for i, out in enumerate(output):
#     print(f"Output {i} shape: {out.shape}")

