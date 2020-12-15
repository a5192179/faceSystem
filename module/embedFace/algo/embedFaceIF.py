
import numpy as np
import mxnet as mx
from sklearn import preprocessing
import cv2
class faceEmbedder:
    def __init__(self, image_size = '112,112', modelPath='./module/embedFace/model/model-r34-amf/model,0', useGPU = False):
        if useGPU:
            ctx = mx.gpu()
        else:
            ctx = mx.cpu()
        _vec = image_size.split(',')
        assert len(_vec)==2
        image_size = (int(_vec[0]), int(_vec[1]))
        image_size = (int(_vec[0]), int(_vec[1]))
        self.model = self.get_model(ctx, image_size, modelPath, 'fc1')

    def get_model(self, ctx, image_size, model_str, layer):
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

    def embedFace(self, face):
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        faceIF = np.transpose(face, (2,0,1))
        input_blob = np.expand_dims(faceIF, axis=0)
        data = mx.nd.array(input_blob)
        db = mx.io.DataBatch(data=(data,))
        self.model.forward(db, is_train=False)
        embedding = self.model.get_outputs()[0].asnumpy()
        embedding = preprocessing.normalize(embedding)
        return embedding