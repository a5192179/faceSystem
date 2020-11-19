import sys
sys.path.append('.')
from module.detectFace.algo import detectFaceCaffe
# from module.detectFace.algo import detectFaceIF
import cv2
from imutils import paths
import numpy as np
import os
import shutil

faceDetector = detectFaceCaffe.faceDetector()
dataset = 'D:/project/touristAnalyse/output/ISCameraLS_000003'
saveFolder = dataset + '/face'
if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)
else:
    shutil.rmtree(saveFolder)
    os.mkdir(saveFolder)
imagePaths = list(paths.list_images(dataset))
for (i, imagePath) in enumerate(imagePaths):
    imgColor = cv2.imread(imagePath)
    imgColor = imgColor[0:450, 0:600, :]
    faces = faceDetector.detectFace(imgColor)
    print('face:', len(faces), 'img:', imagePath)
    i = 0
    for face in faces:
        # face = np.transpose(face, (1,2,0))
        # face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
        cv2.imshow('face', face)
        cv2.waitKey(500)
        imgName = imagePath.split('\\')[-1].split('.')[0] + '-' + str(i) + '.jpg'
        cv2.imwrite(saveFolder+ '/' + imgName, face)
        print(i)
        i += 1
