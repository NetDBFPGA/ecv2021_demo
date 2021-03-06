# Two-stream Action Recognition SOC 🎬

In this project, we implement the two-stream action recognition system on FPGA. Our model has around 10 times less operations than other C3D-based FPGA systems and can achieve near real-time requirement (10~15 FPS) while keeping similar accuracy (on UCF101 and backbone model is ResNet18).

| Architecture | Accuracy    | GOPs | Size(MB) | Backbone |
| -----------  | ----------- | ---- | -------- | -------- |
| F-C3D[1]       |  79%  | 76 | 321 | C3D |
| F-E3D[2]       |  85%  | 12.2 | 8.6 | E3DNet |
| Sun et al.[3]  | 88% | 26.13 | 126 | (2+1)D |
| Ours | 86% | 4.12 | 22.3 | ResNet18 |

## System Overview
![](system_overview.gif)

## Quick Run
We provide the pre-build bitstream and pre-trained model for quick demo. Please refer to [zcu102_demo](https://github.com/NetDBFPGA/ecv2021_demo/tree/master/zcu102_demo)

## Build Bitstream
### Requirements
* Tool Chain: Vivado 2020.1
* License of ZCU102 board

### Build Command
```cmd
#### run hls cnn + bitstream
> make

#### run bitstream only
> make bitstream

#### run hls cnn
> make hls
```

## References
* [1] H. Fan, X. Niu, Q. Liu, and W. Luk. F-c3d: Fpga-based 3-dimensional convolutional neural network. IEEE FPL 2017
* [2] H. Fan, C. Luo, C. Zeng, M. Ferianc, Z. Que, S. Liu, X. Niu, and W. Luk. F-e3d: Fpga-based acceleration of an efficient 3d convolutional neural network for human action recognition. IEEE ASAP 2019
* [3] M. Sun, P. Zhao, M. Gungor, M. Pedram, M. Leeser, and X. Lin. 3d cnn acceleration on fpga using hardware-aware pruning. ACM DAC 2020.
