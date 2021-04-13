import sys
import configparser
import numpy as np

from pynq import Overlay
from pynq import Xlnk

### our define
sys.path.append('../')
import VGG16.fpga_nn as fpga_nn
from VGG16.accelerator import CNN_accelerator

def make_layers(config, in_channel=3, accelerator=None):
    assert config is not None    
    in_height = int(config["DataConfig"]["image_height"])
    in_width = int(config["DataConfig"]["image_width"])
    in_channel = in_channel

    assert accelerator is not None
    acc = accelerator

    layers = []
    #Conv(output channel, input channel, input height, input width, kerSize, stride)
    layers += [fpga_nn.Conv2DPool(32, in_channel, in_height, in_width, ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2DPool(64, 32, int(in_height/2), int(in_width/2), ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2DPool(64, 64, int(in_height/4), int(in_width/4), ker = 3, poolWin = 2, accelerator=acc)]
    
    layers += [fpga_nn.Conv2DPool(64, 64, int(in_height/8), int(in_width/8), ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2DPool(64, 64, int(in_height/16), int(in_width/16), ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2DPool(64, 64, int(in_height/32), int(in_width/32), ker = 3, poolWin = 2, accelerator=acc)]

    # conv output size = (8,8,512)
    layers += [fpga_nn.Flatten(int(in_height/64), int(in_width/64), 64)]
    layers += [fpga_nn.Linear(512,int(in_height/64)*int(in_width/64)*64)]
    layers += [fpga_nn.Linear(101,512, quantize = False)]

    return layers

def make_layers_old(config, in_channel=3, accelerator=None):
    assert config is not None    
    in_height = int(config["DataConfig"]["image_height"])
    in_width = int(config["DataConfig"]["image_width"])
    in_channel = in_channel

    assert accelerator is not None
    acc = accelerator

    layers = []
    #Conv(output channel, input channel, input height, input width, kerSize, stride)
    layers += [fpga_nn.Conv2D(64, in_channel, in_height, in_width, ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2DPool(128, 64, in_height, in_width, ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2D(128, 128, int(in_height/2), int(in_width/2), ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2DPool(256, 128, int(in_height/2), int(in_width/2), ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2D(256, 256, int(in_height/4), int(in_width/4), ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2D(256, 256, int(in_height/4), int(in_width/4), ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2DPool(512, 256, int(in_height/4), int(in_width/4), ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2D(512, 512, int(in_height/8), int(in_width/8), ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2D(512, 512, int(in_height/8), int(in_width/8), ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2DPool(512, 512, int(in_height/8), int(in_width/8), ker = 3, poolWin = 2, accelerator=acc)]

    layers += [fpga_nn.Conv2D(512, 512, int(in_height/16), int(in_width/16), ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2D(512, 512, int(in_height/16), int(in_width/16), ker = 3, s = 1, accelerator=acc)]
    layers += [fpga_nn.Conv2DPool(512, 512, int(in_height/16), int(in_width/16), ker = 3, poolWin = 2, accelerator=acc)]

    # conv output size = (8,8,512)
    layers += [fpga_nn.Flatten(int(in_height/32), int(in_width/32), 512)]
    layers += [fpga_nn.Linear(4096,int(in_height/32)*int(in_width/32)*512)]
    layers += [fpga_nn.Linear(101,4096)]

    return layers

class SimpleNet(CNN_accelerator):
    def __init__(self, config, layers, params_path = None):
        super(SimpleNet, self).__init__(config)
        self.layers = layers
        self.params_path = params_path

        # initialize weight for each layer
        self.init_weight(params_path= params_path)

        # copy weight data to hardware buffer
        self.load_parameters();

    # TODO: load from parameter file
    def init_weight(self, params_path = None):
        for l in self.layers:
            if l.type == "conv" or l.type == "linear":
                l.weight_data = np.random.randint(256,size=l.weight_shape, dtype=np.uint8)
                
def simple_net(config, accelerator):
    layers = make_layers(config, in_channel=3, accelerator=accelerator)
    params_path = "params.path"
    model = SimpleNet(config, layers, params_path = params_path)
    return model

def simple_net_2(config, accelerator):
    layers = make_layers(config, in_channel=20, accelerator=accelerator)
    params_path = "params.path"
    model = SimpleNet(config, layers, params_path = params_path)
    return model

if __name__ == "__main__":

    config_path = './files/config.config'
    model_path = './files/params/ucf101_vgg7/model.pickle'

    config = configparser.ConfigParser()   
    config.read(config_path)

    overlay = Overlay('../files/design_1.bit')

    (in_height, in_width, in_channel) = \
        (256,256,20)

    cnn_acc0 = CNN_accelerator(config, overlay.DoCompute_0)

    vgg7_model = simple_net_2(config, cnn_acc0)

    x = np.random.randint(256,size=(in_height, in_width, in_channel), dtype=np.uint8)

    y = vgg7_model(x)
    