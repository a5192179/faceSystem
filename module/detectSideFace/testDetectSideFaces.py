#coding=utf-8
 
import cv2
import dlib
import sys
sys.path.append('.')
import math
from imutils import paths
import imutils
import shutil
import os
 
dataset = 'D:/project/touristAnalyse/data/testFace'
output = 'D:/project/touristAnalyse/output/sideFace'
imagePaths = list(paths.list_images(dataset))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    "./module/detectSideFace/model/shape_predictor_5_face_landmarks.dat"
)
for (i, imagePath) in enumerate(imagePaths): 
    name = imagePath.split(os.path.sep)[-1]
    img = cv2.imread(imagePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dets = detector(gray, 1)
    for face in dets:
        shape = predictor(img, face)
        # for pt in shape.parts():
        #     pt_pos = (pt.x, pt.y)
        #     cv2.circle(img, pt_pos, 2, (0, 255, 0), 1)
        # cv2.imshow("image", img)
        u1 = shape.parts()[1].x #close to right boundary
        v1 = shape.parts()[1].y
        u3 = shape.parts()[3].x #close to left boundary
        v3 = shape.parts()[3].y
        rate = u1 / (img.shape[1] - u3)
        print('img:', imagePath, 'rate:', rate)
        oriFilePath = imagePath
        newFilePath = output + '/' + str(round(rate, 2)) + '-' + name
        shutil.copy(oriFilePath, newFilePath)