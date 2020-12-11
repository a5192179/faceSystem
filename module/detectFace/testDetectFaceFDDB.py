import sys
sys.path.append('.')
# from module.detectFace.algo import detectFaceCaffe
from module.detectFace.algo import detectFaceIF
import cv2
from imutils import paths
import numpy as np
import os
import shutil
import time
class Statistician:
    def __init__(self):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.TPPath = []
        self.TNPath = []
        self.FPPath = []
        self.FNPath = []

    def judge(self, predict, real, path):
        if predict == real:
            self.TP += 1
            self.TPPath.append(path)
            return True
        else:
            self.FP += 1
            self.FPPath.append(path)
            return False

    def printResult(self):
        print('num:', self.TP + self.FP)
        print('acc', self.TP / (self.TP + self.FP))
        a=1



def readDataSet(path):
    with open(path, "r") as f:
        oriText = f.read()
        text = oriText.split('\n')
        fileInfo = {}
        num = [0, 0, 0, 0, 0]
        i = 0
        while i <  len(text):
            line = text[i]
            if line == '':
                i += 1
                continue
            if line == 'NaN':
                raise BaseException('wrong input')
            if line.find('img_') > 0:
                if int(text[i+1]) > 5:
                    i = i + 2
                    continue
                fileInfo[text[i]] = int(text[i+1])
                num[int(text[i+1]) - 1] += 1
                i = i + 2
                continue
            i += 1
        print('path:', path, 'num:', len(fileInfo))
        print('num list', num)
        return fileInfo

if __name__ == "__main__":
    path = 'D:/project/dataSet/FDDB/FDDB-folds/lishuai.txt'
    fileInfo = readDataSet(path)
    faceDetector = detectFaceIF.faceDetector()
    statistician = Statistician()
    dataset = 'D:/project/dataSet/FDDB/originalPics'

    rightOutputFolder = '../output/testDetectFace/right'
    if not os.path.exists(rightOutputFolder):
        os.mkdir(rightOutputFolder)
    else:
        shutil.rmtree(rightOutputFolder)
        os.mkdir(rightOutputFolder)

    wrongOutputFolder = '../output/testDetectFace/wrong'
    if not os.path.exists(wrongOutputFolder):
        os.mkdir(wrongOutputFolder)
    else:
        shutil.rmtree(wrongOutputFolder)
        os.mkdir(wrongOutputFolder)
    timeStatistic = 0
    imgNum = 0
    for imagePath in fileInfo:
        imgFile = dataset + '/' + imagePath + '.jpg'
        imgColor = cv2.imread(imgFile)
        ts = time.time()
        faces = faceDetector.detectFace(imgColor)
        timeStatistic += time.time() - ts
        imgNum += 1
        real = fileInfo[imagePath]
        predict = len(faces)
        bRight = statistician.judge(predict, real, imagePath)
        # ====================================================
        # i = 0
        # for face in faces:
        #     # face = np.transpose(face, (1,2,0))
        #     # face = cv2.cvtColor(face, cv2.COLOR_RGB2BGR)
        #     # cv2.imshow('face', face)
        #     # cv2.waitKey(1000)
        #     # print(i)
        #     if bRight:
        #         outputFile = rightOutputFolder + '/' + imagePath.split('/')[-1] + '_' + str(real) + '_' + str(predict) + '-' + str(i + 1) + '.jpg'
        #         newFilePath = rightOutputFolder + '/' + imagePath.split('/')[-1] + '_' + str(real) + '_' + str(predict) + '.jpg'
        #     else:
        #         outputFile = wrongOutputFolder + '/' + imagePath.split('/')[-1] + '_' + str(real) + '_' + str(predict) + '-' + str(i + 1) + '.jpg'
        #         newFilePath = wrongOutputFolder + '/' + imagePath.split('/')[-1] + '_' + str(real) + '_' + str(predict) + '.jpg'
        #     cv2.imwrite(outputFile, face)
            
        #     shutil.copy(imgFile, newFilePath)
        #     i += 1
        # if not bRight:
        #     print('face predict:', predict, 'real:', real, 'img:', imagePath)
        # ====================================================
    statistician.printResult()
    print('time:', timeStatistic / imgNum)