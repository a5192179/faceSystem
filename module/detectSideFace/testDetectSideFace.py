#coding=utf-8
 
import cv2
import dlib
import sys
sys.path.append('.')
import math
from imutils import paths
import imutils
import shutil
 
path = "../data/sideFace/159-16.jpg"
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
#人脸分类器
detector = dlib.get_frontal_face_detector()
# 获取人脸检测器
# predictor = dlib.shape_predictor(
#     "./module/detectSideFace/model/shape_predictor_68_face_landmarks.dat"
# )
predictor = dlib.shape_predictor(
    "./module/detectSideFace/model/shape_predictor_5_face_landmarks.dat"
)
 
# face = img
# rec = dlib.rectangle(0,0 + int(face.shape[1] * 0.25),face.shape[0],face.shape[1])
# # rec = dlib.rectangle(0,0,80,130)
# # rec = dlib.rectangle(6,46,96,136)
# shape = predictor(img, rec)  # 寻找人脸的68个标定点
# # 遍历所有点，打印出其坐标，并圈出来
# for pt in shape.parts():
#     pt_pos = (pt.x, pt.y)
#     cv2.circle(img, pt_pos, 2, (0, 255, 0), 1)
# cv2.imshow("image", img)

dets = detector(gray, 1)
for face in dets:
    # face = img
    # rec = dlib.rectangle(0,0,face.shape[0],face.shape[1])
    # shape = predictor(img, rec)  # 寻找人脸的68个标定点
    shape = predictor(img, face)  # 寻找人脸的68个标定点
    # 遍历所有点，打印出其坐标，并圈出来
    for pt in shape.parts():
        pt_pos = (pt.x, pt.y)
        cv2.circle(img, pt_pos, 2, (0, 255, 0), 1)
    cv2.imshow("image", img)
    u0 = shape.parts()[0].x
    v0 = shape.parts()[0].y
    u1 = shape.parts()[1].x #close to right boundary
    v1 = shape.parts()[1].y
    u3 = shape.parts()[3].x #close to left boundary
    v3 = shape.parts()[3].y
    # eyeDist = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)
    # noseLen = math.sqrt(((x1 + x3)/2 - x0)**2 + ((y1 + y3)/2 - y0)**2)
    # rate = eyeDist / noseLen
    rate = u1 / (img.shape[1] - u3)
    print('img:', path, 'rate:', rate)


cv2.waitKey(500)
cv2.destroyAllWindows()