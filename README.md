# Two-stream Action Recognition SOC 🎬
###### tags: `ntu` `netdb`
![](https://img.shields.io/static/v1?label=Zynq_UltraScale+&message=zcu102&color=purple)
![](https://img.shields.io/static/v1?label=Board_OS&message=pynq&color=red)
![](https://img.shields.io/static/v1?label=Vivado&message=2020.1&color=orange)
![](https://img.shields.io/static/v1?label=python&message=3.6&color=blue)
![](https://img.shields.io/static/v1?label=shell&message=bash/zsh&color=green)

We implement the two-stream action recognition system on FPGA. Our implementation can achieve near real-time requirement (10~15 FPS) with competiable accuracy compare to current-state-of-the-art implementations (on UCF101 and backbone model is ResNet18).

| Architecture | Accuracy    | GOPs | Size(MB) | Backbone |
| -----------  | ----------- | ---- | -------- | -------- |
| F-C3D       |  79%  | 76 | 321 | C3D |
| F-E3D       |  85%  | 12.2 | 8.6 | E3DNet |
| Sun et al.  | 88% | 26.13 | 126 | (2+1)D |
| ------    |  -----  | ----- | ----- | -------- |
| Ours | 86% | 4.12 | 22.3 | ResNet18 |
## System Flow
![](https://i.imgur.com/BMqebcv.gif)

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

