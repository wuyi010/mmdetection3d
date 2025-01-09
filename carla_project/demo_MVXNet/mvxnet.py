import time

from demo_MVXNet.MVXNet_DatasetCreate import main_data_mvxnet
from demo_MVXNet.MVXNet_multi_modality_merge import inference_vis

if __name__ == '__main__':
    main_data_mvxnet()
    time.sleep(0.1)
    inference_vis()