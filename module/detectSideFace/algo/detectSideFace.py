import cv2
import dlib
# from imutils.face_utils import rect_to_bb
# from module.detectSideFace.algo.faceAligner import FaceAligner
# import sys
# sys.path.append('.')

class sideFaceDetector:
    def __init__(self, modelPath = './module/detectSideFace/model/shape_predictor_5_face_landmarks.dat', sideFaceThreshold = 0.5):
        self.predictor = dlib.shape_predictor(modelPath)
        self.detector = dlib.get_frontal_face_detector()
        self.sideFaceThreshold = sideFaceThreshold
        # self.faceAlign = FaceAligner(self.predictor)
    
    def isSideFacebyResize(self, img):
        newSize = max(img.shape[0], img.shape[1])
        fv = img.shape[0] / newSize
        fu = img.shape[1] / newSize
        imgResize = cv2.resize(img, (newSize, newSize)) 
        rec = dlib.rectangle(0,0,newSize,newSize)
        shape = self.predictor(imgResize, rec)
        u1 = fu * shape.parts()[1].x #close to right boundary
        v1 = fv * shape.parts()[1].y
        u3 = fu * shape.parts()[3].x #close to left boundary
        v3 = fv * shape.parts()[3].y
        rate = u1 / (img.shape[1] - u3)
        if abs(1 - rate) > self.sideFaceThreshold:
            return True, rate
        else:
            return False, rate

    def align(self, img, gray, dets):
        box = dets[0]
        faceAligned, M = self.faceAlign.align(img, gray, box)
        cv2.imshow('ori', img)
        cv2.imshow('faceAligned', faceAligned)
        cv2.waitKey(0)

    def isSideFacebyDetect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dets = self.detector(gray, 1)
        if len(dets) > 0:
            # self.align(img, gray, dets)
            shape = self.predictor(img, dets[0])
            u1 = shape.parts()[1].x #close to right boundary
            v1 = shape.parts()[1].y
            u3 = shape.parts()[3].x #close to left boundary
            v3 = shape.parts()[3].y
            rate = u1 / (img.shape[1] - u3)
            # rate = abs(u3 - u1) / img.shape[1]
            # threshold = 0.24
            if abs(1 - rate) > self.sideFaceThreshold:
                return True, rate
            else:
                return False, rate
        else:
            return True, 0

    def getFrontFaces(self, faces):
        frontFace = []
        for face in faces:
            bIsSideFace, rate = self.isSideFacebyDetect(face)
            if not bIsSideFace:
                frontFace.append(face)
        return frontFace