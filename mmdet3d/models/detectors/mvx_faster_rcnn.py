# Copyright (c) OpenMMLab. All rights reserved.
from typing import List, Optional, Sequence

import torch
from torch import Tensor
from torch.nn import functional as F

from mmdet3d.registry import MODELS
from .mvx_two_stage import MVXTwoStageDetector


@MODELS.register_module()
class MVXFasterRCNN(MVXTwoStageDetector):
    """Multi-modality VoxelNet using Faster R-CNN."""

    def __init__(self, **kwargs):
        super(MVXFasterRCNN, self).__init__(**kwargs)


@MODELS.register_module()
class DynamicMVXFasterRCNN(MVXTwoStageDetector):
    """Multi-modality VoxelNet using Faster R-CNN and dynamic voxelization."""

    def __init__(self, **kwargs):
        super(DynamicMVXFasterRCNN, self).__init__(**kwargs)

    @torch.no_grad()
    def voxelize(self, points):
        """Apply dynamic voxelization to points.

        Args:
            points (list[torch.Tensor]): Points of each sample.

        Returns:
            tuple[torch.Tensor]: Concatenated points and coordinates.
        """
        coors = []
        # dynamic voxelization only provide a coors mapping
        for res in points:
            res_coors = self.pts_voxel_layer(res)
            coors.append(res_coors)
        points = torch.cat(points, dim=0)
        coors_batch = []
        for i, coor in enumerate(coors):
            coor_pad = F.pad(coor, (1, 0), mode='constant', value=i)
            coors_batch.append(coor_pad)
        coors_batch = torch.cat(coors_batch, dim=0)
        return points, coors_batch

    def extract_pts_feat(
            self,
            points: List[Tensor],
            img_feats: Optional[Sequence[Tensor]] = None,
            batch_input_metas: Optional[List[dict]] = None
    ) -> Sequence[Tensor]:
        """Extract features of points.

        Args:
            points (List[tensor]):  Point cloud of multiple inputs.
            img_feats (list[Tensor], tuple[tensor], optional): Features from
                image backbone.
            batch_input_metas (list[dict], optional): The meta information
                of multiple samples. Defaults to True.

        Returns:
            Sequence[tensor]: points features of multiple inputs
            from backbone or neck.
        """
        if not self.with_pts_bbox:
            return None
        voxels, coors = self.voxelize(points)
        voxel_features, feature_coors = self.pts_voxel_encoder(
            voxels, coors, points, img_feats, batch_input_metas)
        batch_size = coors[-1, 0] + 1
        x = self.pts_middle_encoder(voxel_features, feature_coors, batch_size)
        x = self.pts_backbone(x)
        if self.with_pts_neck:
            x = self.pts_neck(x)
        return x
