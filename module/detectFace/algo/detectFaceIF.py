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
    def __init__(self, modelPath = os.path.join(os.path.dirname(__file__), '../model/mtcnn-model')):
        self.args = Args()
        self.det_threshold = [0.6,0.7,0.8]
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
            points_temp = points[j,:].reshape((2,5)).T
            nimg = face_align.norm_crop(img, points_temp, mode='non-arcface')
            src = np.array([
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041] ], dtype=np.float32 )
            nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2RGB)
            aligned = np.transpose(nimg, (2,0,1))
            aligneds.append(aligned)
        return aligneds