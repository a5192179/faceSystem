import cv2
import dlib
# import sys
# sys.path.append('.')

class sideFaceDetector:
    def __init__(self, modelPath = './module/detectSideFace/model/shape_predictor_5_face_landmarks.dat'):
        self.predictor = dlib.shape_predictor(modelPath)
        self.detector = dlib.get_frontal_face_detector()
    
    def isSideFacebyResize(self, img, threshold = 0.5):
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
        if abs(1 - rate) > threshold:
            return True, rate
        else:
            return False, rate

    def isSideFacebyDetect(self, img, threshold = 0.5):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dets = self.detector(gray, 1)
        if len(dets) > 0:
            shape = self.predictor(img, dets[0])
            u1 = shape.parts()[1].x #close to right boundary
            v1 = shape.parts()[1].y
            u3 = shape.parts()[3].x #close to left boundary
            v3 = shape.parts()[3].y
            rate = u1 / (img.shape[1] - u3)
            if abs(1 - rate) > threshold:
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