import mxnet as mx
import numpy as np
from common import imgProcess

def get_model(ctx, image_size, model_str, layer):
    _vec = model_str.split(',')
    assert len(_vec)==2
    prefix = _vec[0]
    epoch = int(_vec[1])
    print('loading',prefix, epoch)
    sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
    all_layers = sym.get_internals()
    sym = all_layers[layer+'_output']
    model = mx.mod.Module(symbol=sym, context=ctx, label_names = None)
    #model.bind(data_shapes=[('data', (args.batch_size, 3, image_size[0], image_size[1]))], label_shapes=[('softmax_label', (args.batch_size,))])
    model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
    model.set_params(arg_params, aux_params)
    return model

class Args:
    def __init__(self):
        self.image_size = '112,112'
        self.det = int(0)
        self.threshold = 1.24 #ver dist threshold

class ageGenderEstimater:
    def __init__(self, ageScale = 1.0, ga_model = './module/estimateAgeGender/model/gamodel-r50/model, 0'):
        args = Args()
        ctx = mx.cpu()
        _vec = args.image_size.split(',')
        assert len(_vec)==2
        image_size = (int(_vec[0]), int(_vec[1]))
        self.ageScale = ageScale
        self.ga_model = get_model(ctx, image_size, ga_model, 'fc1')

    def estimateAgeGender(self, imgColor):
        aligned = imgProcess.tansBGR2ISFormat(imgColor, [0, 0, imgColor.shape[1], imgColor.shape[0]], imgColor)
        input_blob = np.expand_dims(aligned, axis=0)
        data = mx.nd.array(input_blob)
        db = mx.io.DataBatch(data=(data,))
        self.ga_model.forward(db, is_train=False)
        ret = self.ga_model.get_outputs()[0].asnumpy()
        g = ret[:,0:2].flatten()
        gender = np.argmax(g)
        a = ret[:,2:202].reshape( (100,2) )
        a = np.argmax(a, axis=1)
        age = int(sum(a) * self.ageScale)
        if gender == 1:
            gender = 'Male'
        else:
            gender = 'Female'
            age = int(age * self.ageScale)
        return str(age), gender