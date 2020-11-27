import cv2
# import keras
import numpy as np
import imutils
from imutils import paths
import sys
sys.path.append('.')
from algo import detectSideFace
import time


sideFaceDetector = detectSideFace.sideFaceDetector(sideFaceThreshold = 0.5)
dataset = 'D:/project/touristAnalyse/data/inclined'
imagePaths = list(paths.list_images(dataset))
for (i, imagePath) in enumerate(imagePaths):
    imgColor = cv2.imread(imagePath)
    ts = time.time()
    faces = sideFaceDetector.getFrontFaces([imgColor])
    print("time:", time.time() - ts)
    # cv2.putText(imgColor, age+gender, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 1, cv2.LINE_AA)
    # cv2.imshow('age', imgColor)
    # cv2.waitKey(2000)