
"""

漏检率：         RM = undetected  / total
误检率：         RF = falsepositive / total
               RM = 0.25*RM_YOLO +0.25*RM_PP + 0.5*RM_BEV
               RF = 0.25*RF_YOLO +0.25*RF_PP + 0.5*RF_BEV
传感器配置性能：  P = 0.7*RM + 0.3*RF

"""

import numpy as np

import torch

# 创建张量
total = torch.tensor(9.0)
weights = torch.tensor([0.25, 0.25, 0.5])
weights2 = torch.tensor([0.7, 0.3])
undetected_falsepositive = torch.tensor([
     [1, 6,  4],   #A: undetected
     [0, 1,  0],   #A: falsepositive
     [0, 6,  0],   #B: undetected
     [0, 1,  0]    #B: falsepositive
    ])
RM_RF_single = undetected_falsepositive / total
RM_RF =  torch.matmul(RM_RF_single, weights)
tensor_2d = RM_RF.reshape(2, 2)
P =  torch.matmul(tensor_2d, weights2)
print("城市：")
print("\t已经发布方案")
print("\t\tyolo  RM:",RM_RF_single[0][0].item(),"RF=",RM_RF_single[1][0].item())
print("\t\tpoinp RM:",RM_RF_single[0][1].item(),"RF=",RM_RF_single[1][1].item())
print("\t\tbevf  RM:",RM_RF_single[0][2].item(),"RF=",RM_RF_single[1][2].item())
print("\t\t漏检率=",RM_RF[0].item()," 误检率=",RM_RF[1].item(),"P=",P[0].item(),)
print("\t优化算法方案")
print("\t\tyolo  RM:",RM_RF_single[2][0].item(),"RF=",RM_RF_single[3][0].item())
print("\t\tpoinp RM:",RM_RF_single[2][1].item(),"RF=",RM_RF_single[3][1].item())
print("\t\tbevf  RM:",RM_RF_single[2][2].item(),"RF=",RM_RF_single[3][2].item())
print("\t\t漏检率=",RM_RF[2].item()," 误检率=",RM_RF[3].item(),"P=",P[1].item())


# 创建张量
total = torch.tensor(7.0)
weights = torch.tensor([0.25, 0.25, 0.5])
weights2 = torch.tensor([0.7, 0.3])
undetected_falsepositive = torch.tensor([
     [2, 2,  2],  [0, 0,  0],   #A: undetected #A: falsepositive
     [1, 0,  0],  [0, 0,  0]     #B: undetected #B: falsepositive

    ])
RM_RF_single = undetected_falsepositive / total
RM_RF =  torch.matmul(RM_RF_single, weights)


tensor_2d = RM_RF.reshape(2, 2)
P =  torch.matmul(tensor_2d, weights2)
print("高速：")
print("\t已经发布方案")
print("\t\tyolo  RM:",RM_RF_single[0][0].item(),"RF=",RM_RF_single[1][0].item())
print("\t\tpoinp RM:",RM_RF_single[0][1].item(),"RF=",RM_RF_single[1][1].item())
print("\t\tbevf  RM:",RM_RF_single[0][2].item(),"RF=",RM_RF_single[1][2].item())
print("\t\t漏检率=",RM_RF[0].item()," 误检率=",RM_RF[1].item(),"P=",P[0].item(),)
print("\t优化算法方案")
print("\t\tyolo  RM:",RM_RF_single[2][0].item(),"RF=",RM_RF_single[3][0].item())
print("\t\tpoinp RM:",RM_RF_single[2][1].item(),"RF=",RM_RF_single[3][1].item())
print("\t\tbevf  RM:",RM_RF_single[2][2].item(),"RF=",RM_RF_single[3][2].item())
print("\t\t漏检率=",RM_RF[2].item()," 误检率=",RM_RF[3].item(),"P=",P[1].item())