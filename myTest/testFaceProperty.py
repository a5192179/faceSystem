import cv2
# import keras
import numpy as np
import imutils
from imutils import paths
import sys
sys.path.append('.')
# sys.path.append('./module/estimateAgeGender/algo')
# import estimateAgeGender
# from algo import estimateAgeGender
from module.estimateAgeGender.algo import estimateAgeGenderIF
import time
from module.detectFace.algo import detectFaceCaffe

def resizeImgIntoFrame(img, H, W):
    imgH = img.shape[0]
    imgW = img.shape[1]
    rate = max(imgH/H, imgW/W)
    newH = int(imgH / rate)
    newW = int(imgW / rate)
    imgNew = cv2.resize(img, (newW, newH))
    return imgNew


# ageGenderEstimater = estimateAgeGender.ageGenderEstimater()
faceDetector = detectFaceCaffe.faceDetector()
ageGenderEstimater = estimateAgeGenderIF.ageGenderEstimater()
dataset = 'D:/project/faceProperty/data/sameMale'
# dataset = 'D:/project/AiBox/data/debug1102'
# dataset = 'D:/project/touristAnalyse/data/testWH'
imagePaths = list(paths.list_images(dataset))
for (i, imagePath) in enumerate(imagePaths):
    imgColor = cv2.imread(imagePath)
    faces = faceDetector.detectFace(imgColor)
    ts = time.time()
    for face in faces:
        age, gender = ageGenderEstimater.estimateAgeGender(face)
        print("img:", imagePath[-10:], "age:", age, "gender:", gender)
        # cv2.putText(imgColor, age+gender, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 1, cv2.LINE_AA)
        faceShow = resizeImgIntoFrame(face, 200, 200)
        cv2.putText(faceShow, gender, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 1, cv2.LINE_AA)
        cv2.imshow('age', faceShow)
        cv2.waitKey(0)


# import sys
# sys.path.append('.')
# from module.detectFace.algo import detectFaceCaffe
# # from module.detectFace.algo import detectFaceIF
# import cv2
# from imutils import paths
# import numpy as np

# faceDetector = detectFaceCaffe.faceDetector()
# dataset = 'D:/project/faceDetect/data/holeImage'
# imagePaths = list(paths.list_images(dataset))
# for (i, imagePath) in enumerate(imagePaths):
#     imgColor = cv2.imread(imagePath)
#     faces = faceDetector.detectFace(imgColor)
#     print('face:', len(faces), 'img:', imagePath)
#     i = 0
#     for face in faces:
#         # face = np.transpose(face, (1,2,0))
#         # face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
#         cv2.imshow('face', face)
#         cv2.waitKey(1000)
#         print(i)
#         i += 1
