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
output = 'D:/project/touristAnalyse/output/sideFaceResize'
imagePaths = list(paths.list_images(dataset))
# detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    "./module/detectSideFace/model/shape_predictor_5_face_landmarks.dat"
)
for (i, imagePath) in enumerate(imagePaths): 
    name = imagePath.split(os.path.sep)[-1]
    img = cv2.imread(imagePath)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    newSize = max(img.shape[0], img.shape[1])
    fv = img.shape[0] / newSize
    fu = img.shape[1] / newSize
    imgResize = cv2.resize(img, (newSize, newSize)) 
    rec = dlib.rectangle(0,0,newSize,newSize)
    # dets = detector(gray, 1)
    shape = predictor(imgResize, rec)
    # for pt in shape.parts():
    #     pt_pos = (pt.x, pt.y)
    #     cv2.circle(img, pt_pos, 2, (0, 255, 0), 1)
    # cv2.imshow("image", img)
    u1 = fu * shape.parts()[1].x #close to right boundary
    v1 = fv * shape.parts()[1].y
    u3 = fu * shape.parts()[3].x #close to left boundary
    v3 = fv * shape.parts()[3].y
    rate = u1 / (img.shape[1] - u3)
    print('img:', imagePath, 'rate:', rate)
    oriFilePath = imagePath
    newFilePath = output + '/' + str(round(rate, 2)) + '-' + name
    shutil.copy(oriFilePath, newFilePath)