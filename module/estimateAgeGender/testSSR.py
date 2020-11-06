import cv2
# import keras
import numpy as np
import imutils
from imutils import paths
import sys
# sys.path.append('./module/estimateAgeGender/algo')
# import estimateAgeGender
from algo import estimateAgeGender
import time


ageGenderEstimater = estimateAgeGender.ageGenderEstimater()
# dataset = 'D:/project/faceProperty/data/old'
dataset = 'D:/project/AiBox/data/debug1102'
imagePaths = list(paths.list_images(dataset))
for (i, imagePath) in enumerate(imagePaths):
    imgColor = cv2.imread(imagePath)
    ts = time.time()
    age, gender = ageGenderEstimater.estimateAgeGenderbyArray(imgColor)
    print("time:", time.time() - ts)
    print("img:", imagePath[-10:], "age:", age, "gender:", gender)
    cv2.putText(imgColor, age+gender, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)
    cv2.imshow('age', imgColor)
    cv2.waitKey(2000)