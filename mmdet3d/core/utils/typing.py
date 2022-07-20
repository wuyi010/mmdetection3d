# Copyright (c) OpenMMLab. All rights reserved.
"""Collecting some commonly used type hint in MMDetection3D."""
from typing import Dict, List, Optional, Tuple, Union

import torch
from mmengine.config import ConfigDict
from mmengine.data import InstanceData

from ..bbox.samplers import SamplingResult
from ..data_structures import Det3DDataSample

# Type hint of config data
ConfigType = Union[ConfigDict, dict]
OptConfigType = Optional[ConfigType]

# Type hint of one or more config data
MultiConfig = Union[ConfigType, List[ConfigType]]
OptMultiConfig = Optional[MultiConfig]

InstanceList = List[InstanceData]
OptInstanceList = Optional[InstanceList]

SampleList = List[Det3DDataSample]
OptSampleList = Optional[SampleList]

SamplingResultList = List[SamplingResult]

OptSamplingResultList = Optional[SamplingResultList]

ForwardResults = Union[Dict[str, torch.Tensor], List[Det3DDataSample],
                       Tuple[torch.Tensor], torch.Tensor]
