import cv2
import os
import sys
sys.path.append('.')
from module.detectFace.algo import detectFaceCaffe

path = '../data/testFaceIF'
saveFolder = '../data/testFaceCF'
foldersList = []
foldersList.append(path)
imgList = []
faceDetector = detectFaceCaffe.faceDetector()
while len(foldersList) > 0:
    tempRootDir = foldersList[0]
    files = os.listdir(tempRootDir)
    for filename in files:
        filePath = tempRootDir + '/' + filename
        if os.path.isdir(filePath):
            foldersList.append(filePath)
        else:
            # ==========================
            if filename.endswith('jpg'):
                imgColor = cv2.imread(filePath)
                faces = faceDetector.detectFace(imgColor)
                saveFolderSub = saveFolder + '/' + filePath.split('testFaceIF')[-1].split('/')[1]
                if not os.path.exists(saveFolderSub):
                    os.mkdir(saveFolderSub)
                if len(faces) > 1:
                    maxFaceIndex = 0
                    maxLenth = 0
                    for i in range(len(faces)):
                        face = faces[i]
                        if face.shape[1] > maxLenth:
                            maxFaceIndex = i
                            maxLenth = face.shape[1]
                    for i in range(len(faces)):
                        face = faces[i]
                        if i == maxFaceIndex:
                            saveImg = saveFolder + filePath.split('testFaceIF')[-1]
                            cv2.imwrite(saveImg, face)
                        else:
                            saveImg = saveFolderSub + filePath.split('/')[-1].split('.')[0] + '-' + str(i) + '.jpg'
                            cv2.imwrite(saveImg, face)
            # ==========================
    print(tempRootDir + ' dir end')
    foldersList.pop(0)

