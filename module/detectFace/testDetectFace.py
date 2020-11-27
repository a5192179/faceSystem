import sys
sys.path.append('.')
# from module.detectFace.algo import detectFaceCaffe
from module.detectFace.algo import detectFaceIF
import cv2
from imutils import paths
import numpy as np

faceDetector = detectFaceIF.faceDetector()
dataset = 'D:/project/faceDetect/data/holeImage'
imagePaths = list(paths.list_images(dataset))
for (i, imagePath) in enumerate(imagePaths):
    imgColor = cv2.imread(imagePath)
    faces = faceDetector.detectFace(imgColor)
    print('face:', len(faces), 'img:', imagePath)
    i = 0
    for face in faces:
        face = np.transpose(face, (1,2,0))
        face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
        cv2.imshow('face', face)
        cv2.waitKey(1000)
        print(i)
        i += 1

    