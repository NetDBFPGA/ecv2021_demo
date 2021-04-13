
from math import floor, ceil
import numpy as np

## our define
from VGG16.accelerator import CNN_accelerator
import VGG16.conv_operation as co


class Conv2D(CNN_accelerator):
    def __init__(self, out_channel, in_channel, in_height, in_width,\
        multiplier=1, zp_x=0, zp_w=0, zp_x_next=0,\
        ker=3, s=1, accelerator=None, config=None):

        assert accelerator is not None
        super(Conv2D, self).__init__(config)

        self.type = "conv"
        self.out_channel = out_channel
        self.in_channel = in_channel
        self.in_height = in_height
        self.in_width = in_width
        self.out_height = in_height
        self.out_width = in_width
        self.ker = ker
        self.s = s
        self.weight_shape = (out_channel, in_channel, ker, ker)
        self.weight_data = None
        
        self.accelerator = accelerator

        self.multiplier = multiplier
        self.zp_x = zp_x
        self.zp_w = zp_w
        self.zp_x_next = zp_x_next

        self.quantize = True
        
        self.ofm_buff, self.wgt_buff = \
            self.accelerator.mem_alloc(max(out_channel, self.To)\
            , max(in_channel, self.Ti), self.out_height, self.out_width, ker)

    def __call__(self, ifm_buff):
        # print("executing conv2d")
        self.ifm_buff = ifm_buff
        self.accelerator.setting(self.ofm_buff,\
                                 self.ifm_buff,\
                                 self.wgt_buff,\
                                 self.out_channel,\
                                 self.in_channel,\
                                 self.in_height,\
                                 self.in_width,\
                                 self.multiplier,\
                                 self.zp_x,\
                                 self.zp_w,\
                                 self.zp_x_next,\
                                 self.ker,\
                                 self.s)
        self.accelerator.execute()
        return self.ofm_buff

class Conv2DPool(CNN_accelerator):
    def __init__(self, out_channel, in_channel, in_height, in_width,\
        multiplier=1, zp_x=0, zp_w=0, zp_x_next=0,\
        ker=3, s=1, poolWin = 2, accelerator=None, config=None):
        assert accelerator is not None
        super(Conv2DPool, self).__init__(config)

        self.type = "conv"
        self.out_channel = out_channel
        self.in_channel = in_channel
        self.in_height = in_height
        self.in_width = in_width
        self.out_height = int(ceil(in_height/poolWin))
        self.out_width = int(ceil(in_width/poolWin))
        self.ker = ker
        self.s = s
        self.poolWin = poolWin
        self.weight_shape = (out_channel, in_channel, ker, ker)
        self.weight_data = None
        
        self.accelerator = accelerator

        self.multiplier = multiplier
        self.zp_x = zp_x
        self.zp_w = zp_w
        self.zp_x_next = zp_x_next

        self.quantize = True
        
        self.ofm_buff, self.wgt_buff = \
            self.accelerator.mem_alloc(max(out_channel, self.To)\
                , max(in_channel, self.Ti), self.out_height, self.out_width, ker)

    def __call__(self, ifm_buff):
        # print("executing conv2dPool")
        self.ifm_buff = ifm_buff
        self.accelerator.setting(self.ofm_buff,\
                                 self.ifm_buff,\
                                 self.wgt_buff,\
                                 self.out_channel,\
                                 self.in_channel,\
                                 self.in_height,\
                                 self.in_width,\
                                 self.multiplier,\
                                 self.zp_x,\
                                 self.zp_w,\
                                 self.zp_x_next,\
                                 poolWin = self.poolWin)
        self.accelerator.execute()
        return self.ofm_buff
    
class Linear(CNN_accelerator):
    def __init__(self, out_channel, in_channel,\
        multiplier=1, zp_x=0, zp_w=0, zp_x_next=0, quantize=True):
        super(Linear, self).__init__()

        self.type = "linear"
        self.out_channel = out_channel
        self.in_channel = in_channel
        self.in_height = 1
        self.in_width = 1
        self.out_height = 1
        self.out_width = 1
        self.ker = 1
        self.weight_shape = (out_channel, in_channel)
        self.weight_data = None

        self.multiplier = multiplier
        self.zp_x = zp_x
        self.zp_w = zp_w
        self.zp_x_next = zp_x_next

        self.quantize = quantize

        # self.ofm_buff, self.wgt_buff = \
        # self.mem_alloc(max(out_channel, self.To)\
        #   , max(in_channel, self.Ti), self.out_height, self.out_width, self.ker)

    def __call__(self, feature):
        # print("executing Fully Connected Layer")
        # feature: (1, in_channel * in_height * in_width)
        # wgt: (out_channel, in_channel * in_height * in_width)
        if self.quantize:
            return co.sw_linear_quant(feature, self.weight_data, \
                self.multiplier, self.zp_x, self.zp_w, self.zp_x_next)
        else:
            # dequantize
            deq_feature = self.multiplier*(feature.astype(np.float32)-self.zp_x)
            return co.sw_linear(deq_feature, self.weight_data)

class Flatten(CNN_accelerator):
    def __init__(self, in_height, in_width, in_channel):
        super(Flatten, self).__init__()
        
        self.type = "flatten"
        self.in_height = in_height
        self.in_width = in_width
        self.in_channel = in_channel

        self.out_height = 1
        self.out_width = 1
        self.out_channel = self.in_height * self.in_width * self.in_channel

        self.weight_shape = (in_height, in_width, in_channel)
        # self.tile_depth = int(in_height*in_width)

    def __call__(self, feature_buff):
        # print("executing Flatten")
        # convert to row major feature map(channel, height, width)
        return co.convertOFMOutput(\
                feature_buff, feature_buff.shape[0], self.WORD_LENGTH\
                , self.in_channel, self.in_height, self.in_width, Ti = self.Ti)\
            .reshape((self.in_channel * self.in_height * self.in_width, -1))

        # buffer_depth = hw_buffer.shape[0]

        # # TODO: padding zero
        # num_tile = int(ceil(buffer_depth/self.tile_depth))
        # return np.transpose(\
        #   hw_buffer.reshape((num_tile,self.tile_depth,self.WORD_LENGTH)),(0,2,1))\
        # .reshape((buffer_depth,self.WORD_LENGTH))
