import sys
sys.path.append('.')
# from module.detectFace.algo import detectFaceCaffe
from module.detectFace.algo import detectFaceIF
from module.estimateAgeGender.algo import estimateAgeGenderIF
import cv2
import numpy as np
import os
import pickle
import math
import time

class GenderStatistician:
    def __init__(self):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.TPPath = []
        self.TNPath = []
        self.FPPath = []
        self.FNPath = []
        self.realMale = 0
        self.realFemale = 0

    def judge(self, predict, real, path):
        if real == 1:
            self.realMale += 1
        else:
            self.realFemale += 1
        if predict == 1:
            if predict == real:
                self.TP += 1
                self.TPPath.append(path)
            else:
                self.FP += 1
                self.FPPath.append(path)
        else:
            if predict != real:
                self.FN += 1
                self.FNPath.append(path)
            else:
                self.TN += 1
                self.TNPath.append(path)

    def printResult(self):
        print('gender')
        print('TP:', self.TP, 'FP:', self.FP, 'TN:', self.TN, 'FN:', self.FN)
        print('acc', (self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN))
        print('recall', (self.TP) / (self.TP + self.FN))
        print('realMale:', self.realMale, 'female:', self.realFemale)
        a=1
    
class AgeStatistician:
    def __init__(self):
        self.right = 0
        self.wrong = 0
        self.diff = []
        self.num = 0
        self.error = 0
        self.rightPath = []
        self.wrongPath = []
        self.threshold = 10
        self.age = {}


    def judge(self, predict, real, path):
        if str(real) in self.age:
            self.age[str(real)] += 1
        else:
            self.age[str(real)] = 1
        diff = predict - real
        if abs(diff) <= self.threshold:
            self.right += 1
            self.rightPath.append(path)
        else:
            self.wrong += 1
            self.wrongPath.append(path)
        self.diff.append(diff)
        self.error += abs(diff)
        self.num += 1

    def printResult(self):
        print('age')
        print('right', self.right, 'wrong', self.wrong)
        print('acc', self.right / (self.right + self.wrong))
        print('mean:', self.error / self.num)
        for age in self.age:
            print('age:', age, 'num', self.age[age])
        a=1


# def readDataSet(path, txtFomat, errorList):
#     with open(path, "r") as f:
#         oriText = f.read()
#         text = oriText.split('\n')
#         result = []
#         i = 0
#         errorNum = 0
#         for numStr in text:
#             if numStr == '':
#                 continue
#             if numStr == 'NaN':
#                 if errorList.count(i) == 0:
#                     errorList.append(i)
#                     i += 1
#                     errorNum += 1
#                     if txtFomat == 'str':
#                         result.append('NaN')
#                     elif txtFomat == 'int' or txtFomat == 'float':
#                         result.append(0)
#                 continue
#             if txtFomat == 'str':
#                 result.append(numStr)
#             elif txtFomat == 'int':
#                 result.append(int(numStr))
#             elif txtFomat == 'float':
#                 result.append(float(numStr))
#             i += 1
#         print('path:', path, 'errorNum:', errorNum)
#         return result

# def matlabData2PythonYear(matDay):
#     pythonYear = 1970 + (matDay - 719529)/365
#     return round(pythonYear)

# def getAge(errorList, dobList, photoTakenList):
#     i = 0
#     ageList = []
#     for dob in dobList:
#         if errorList.count(i) > 0:
#             ageList.append(-1)
#             i += 1
#             continue
#         dob = matlabData2PythonYear(dob)
#         photoTaken = photoTakenList[i]
#         age = photoTaken - dob
#         ageList.append(age)
#         i += 1
#     print('get age num:', i)
#     return ageList

# def cleanData(dataSetFolder, faceDetector, errorList, imgListOri, ageListOri, genderListOri):
#     imgList = []
#     ageList = []
#     genderList = []
#     i = 0
#     finalNum = 0
#     for imgPath in imgListOri:
#         # if imgPath.find('11064319_1971-10-31_2009.jpg') > 0:
#         #     a = 1
#         if errorList.count(i) > 0:
#             i += 1
#             print('input:', i, 'final:', finalNum, 'pass by error')
#             continue
#         if ageListOri[i] < 0:
#             i += 1
#             print('input:', i, 'final:', finalNum, 'pass by age')
#             continue
#         imagePath = dataSetFolder + '/' + imgPath
#         imgColor = cv2.imread(imagePath)
#         faces = faceDetector.detectFace(imgColor)
#         if len(faces) < 1:
#             i += 1
#             print('input:', i, 'final:', finalNum, 'pass by no face')
#             continue
#         if len(faces) > 1:
#             i += 1
#             print('input:', i, 'final:', finalNum, 'pass by too more face')
#             continue
#         imgList.append(imgPath)
#         ageList.append(ageListOri[i])
#         genderList.append(genderListOri[i])
#         i += 1
#         finalNum += 1
#         if finalNum >= 2000:
#             break
#     print('input:', i, 'final:', finalNum)
#     savePath = dataSetFolder + '/imgList.txt'
#     f = open(savePath, "wb")
#     f.write(pickle.dumps(imgList))
#     f.close()
#     savePath = dataSetFolder + '/ageList.txt'
#     f = open(savePath, "wb")
#     f.write(pickle.dumps(ageList))
#     f.close()
#     savePath = dataSetFolder + '/genderList.txt'
#     f = open(savePath, "wb")
#     f.write(pickle.dumps(genderList))
#     f.close()
#     return imgList, ageList, genderList

def getDataSet(dataSetFolder):
    foldersList = []
    foldersList.append(dataSetFolder)
    imgList = []
    ageList = []
    genderList = []
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
                    infoStr = tempRootDir.split('/')[-1]
                    infoList = infoStr.split('-')
                    gender = int(infoList[1])
                    age = int(infoList[2])
                    imgList.append(filePath)
                    ageList.append(age)
                    genderList.append(gender)
                # ==========================
        print(tempRootDir + ' dir end')
        foldersList.pop(0)
    return imgList, ageList, genderList

def SMD2(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    '''
    :param img:narray 二维灰度图像
    :return: float 图像约清晰越大
    '''
    shape = np.shape(img)
    out = 0
    for x in range(0, shape[0]-1):
        for y in range(0, shape[1]-1):
            out+=math.fabs(int(img[x,y])-int(img[x+1,y]))*math.fabs(int(img[x,y]-int(img[x,y+1])))
    return out / (shape[0] * shape[1])

if __name__ == "__main__":
    # dataSetFolder = 'D:/project/dataSet/imdb/wiki_crop'
    dataSetFolder = 'D:/project/touristAnalyse/data/testFaceIF'
    # dataSetFolder = 'D:/project/dataSet/CACD/my'
    imgList, ageList, genderList = getDataSet(dataSetFolder)
    # faceDetector = detectFaceIF.faceDetector()
    ageGenderEstimater = estimateAgeGenderIF.ageGenderEstimater()
    genderStatistician = GenderStatistician()
    ageStatistician = AgeStatistician()
    i = 0
    timeStatistics = 0
    for imgPath in imgList:
        # imagePath = dataSetFolder + '/' + imgPath
        imagePath = imgPath
        face = cv2.imread(imagePath)
        # faces = faceDetector.detectFace(imgColor)
        # face = faces[0]
        ts = time.time()
        age, gender = ageGenderEstimater.estimateAgeGender(face)
        timeStatistics += (time.time() - ts)
        print('error:', int(age) - ageList[i])
        # print('error:', int(age) - ageList[i], 'smd2:', SMD2(face))
        # =================================================================================
        # cv2.putText(face, age+gender, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 1, cv2.LINE_AA)
        # cv2.putText(face, str(ageList[i])+str(genderList[i]), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 1, cv2.LINE_AA)
        # cv2.imshow('age', face)
        # cv2.waitKey(400)
        # =================================================================================
        if gender == 'Male':
            gender = 1
        else:
            gender = 0
        ageStatistician.judge(int(age), ageList[i], imagePath)
        genderStatistician.judge(gender, genderList[i], imagePath)
        i += 1
        if i == 100:
            print(i)
            # break
    print('time:', timeStatistics / i)
    ageStatistician.printResult()
    genderStatistician.printResult()
