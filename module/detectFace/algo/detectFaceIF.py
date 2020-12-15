import os
import cv2
import mxnet as mx
import numpy as np
from module.detectFace.algo import face_align
from module.detectFace.algo.mtcnn_detector import MtcnnDetector
class Args:
    def __init__(self):
        self.image_size = '112,112'
        self.det = int(0)
        self.threshold = 1.24 #ver dist threshold

class faceDetector:
    def __init__(self, modelPath = os.path.join(os.path.dirname(__file__), '../model/mtcnn-model'), useGPU = False):
        self.args = Args()
        self.det_threshold = [0.6,0.7,0.8]
        if useGPU:
            ctx = mx.gpu()
        else:
            ctx = mx.cpu()
        if self.args.det==0:
            detector = MtcnnDetector(model_folder=modelPath, ctx=ctx, num_worker=1, accurate_landmark = True, threshold=self.det_threshold)
        else:
            detector = MtcnnDetector(model_folder=modelPath, ctx=ctx, num_worker=1, accurate_landmark = True, threshold=[0.0,0.0,0.2])
        self.detector = detector

    def detectFace(self, img):
        ret = self.detector.detect_face(img, det_type = self.args.det)
        if ret is None:
            return []
        bbox, points = ret
        if bbox.shape[0] == 0:
            return []
        aligneds = []
        for j in range(bbox.shape[0]):
            bbox_temp = bbox[j,0:4] # only get the first face
            if bbox_temp[2] - bbox_temp[0] < 40 or bbox_temp[3] - bbox_temp[1] < 40:
                continue
            points_temp = points[j,:].reshape((2,5)).T
            nimg = face_align.norm_crop(img, points_temp, mode='non-arcface')
            # nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2RGB)
            # aligned = np.transpose(nimg, (2,0,1))
            # aligneds.append(aligned)
            aligneds.append(nimg)
        return aligneds