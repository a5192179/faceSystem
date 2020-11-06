import dlib
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import numpy as np
import cv2

class faceDetector:
    def __init__(self, modelPath = './module/detectFace/model/shape_predictor_68_face_landmarks.dat'):
        # load our serialized face detector from disk
        print("[INFO] loading face detector...")
        self.detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(modelPath)
        self.fa = FaceAligner(predictor)

    def detectFace(self, img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # face detector
        rects = self.detector(imgGray, 1)
        (h, w) = img.shape[:2]
        # loop over the detections
        faces = []
        if rects.__len__() > 0:
            for rect in rects:
                (fX, fY, fW, fH) = rect_to_bb(rect)
                face = self.fa.align(img, imgGray, rect)
                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue
                faces.append(face)
        # faceOri = img[fY:fY+fH+1, fX:fX+fW+1, :]
        # cv2.imshow('ori', faceOri)
        # cv2.imshow('new', face)
        # cv2.waitKey(0)
        return faces
                
