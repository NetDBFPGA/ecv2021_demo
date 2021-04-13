# Two-stream Action Recognition SOC 🎬
###### tags: `ntu` `netdb`
![](https://img.shields.io/static/v1?label=Zynq_UltraScale+&message=zcu102&color=purple)
![](https://img.shields.io/static/v1?label=Board_OS&message=pynq&color=red)
![](https://img.shields.io/static/v1?label=Vivado&message=2020.1&color=orange)
![](https://img.shields.io/static/v1?label=python&message=3.6&color=blue)
![](https://img.shields.io/static/v1?label=shell&message=bash/zsh&color=green)

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

