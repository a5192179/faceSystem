import sys
sys.path.append('.')
# from module.detectFace.algo import detectFaceCaffe
from module.detectFace.algo import detectFaceIF
from module.estimateAgeGender.algo import estimateAgeGenderIF
import cv2
import numpy as np
import os
import pickle

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

    def judge(self, predict, real, path):
        if predict == 1:
            if predict == real:
                self.TP += 1
                self.TPPath.append(path)
            else:
                self.FP += 1
                self.FPPath.append(path)
        else:
            if predict == real:
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
        a=1
    
class AgeStatistician:
    def __init__(self):
        self.right = 0
        self.wrong = 0
        self.diff = []
        self.rightPath = []
        self.wrongPath = []
        self.threshold = 5

    def judge(self, predict, real, path):
        diff = predict - real
        if abs(diff) <= self.threshold:
            self.right += 1
            self.rightPath.append(path)
        else:
            self.wrong += 1
            self.wrongPath.append(path)
        self.diff.append(diff)

    def printResult(self):
        print('age')
        print('right', self.right, 'wrong', self.wrong)
        print('acc', self.right / (self.right + self.wrong))


def readDataSet(path, txtFomat, errorList):
    with open(path, "r") as f:
        oriText = f.read()
        text = oriText.split('\n')
        result = []
        i = 0
        errorNum = 0
        for numStr in text:
            if numStr == '':
                continue
            if numStr == 'NaN':
                if errorList.count(i) == 0:
                    errorList.append(i)
                    i += 1
                    errorNum += 1
                    if txtFomat == 'str':
                        result.append('NaN')
                    elif txtFomat == 'int' or txtFomat == 'float':
                        result.append(0)
                continue
            if txtFomat == 'str':
                result.append(numStr)
            elif txtFomat == 'int':
                result.append(int(numStr))
            elif txtFomat == 'float':
                result.append(float(numStr))
            i += 1
        print('path:', path, 'errorNum:', errorNum)
        return result

def matlabData2PythonYear(matDay):
    pythonYear = 1970 + (matDay - 719529)/365
    return round(pythonYear)

def getAge(errorList, dobList, photoTakenList):
    i = 0
    ageList = []
    for dob in dobList:
        if errorList.count(i) > 0:
            ageList.append(-1)
            i += 1
            continue
        dob = matlabData2PythonYear(dob)
        photoTaken = photoTakenList[i]
        age = photoTaken - dob
        ageList.append(age)
        i += 1
    print('get age num:', i)
    return ageList

def cleanData(dataSetFolder, faceDetector, errorList, imgListOri, ageListOri, genderListOri):
    imgList = []
    ageList = []
    genderList = []
    i = 0
    finalNum = 0
    for imgPath in imgListOri:
        # if imgPath.find('11064319_1971-10-31_2009.jpg') > 0:
        #     a = 1
        if errorList.count(i) > 0:
            i += 1
            print('input:', i, 'final:', finalNum, 'pass by error')
            continue
        if ageListOri[i] < 0:
            i += 1
            print('input:', i, 'final:', finalNum, 'pass by age')
            continue
        imagePath = dataSetFolder + '/' + imgPath
        imgColor = cv2.imread(imagePath)
        faces = faceDetector.detectFace(imgColor)
        if len(faces) < 1:
            i += 1
            print('input:', i, 'final:', finalNum, 'pass by no face')
            continue
        if len(faces) > 1:
            i += 1
            print('input:', i, 'final:', finalNum, 'pass by too more face')
            continue
        imgList.append(imgPath)
        ageList.append(ageListOri[i])
        genderList.append(genderListOri[i])
        i += 1
        finalNum += 1
        if finalNum >= 2000:
            break
    print('input:', i, 'final:', finalNum)
    savePath = dataSetFolder + '/imgList.txt'
    f = open(savePath, "wb")
    f.write(pickle.dumps(imgList))
    f.close()
    savePath = dataSetFolder + '/ageList.txt'
    f = open(savePath, "wb")
    f.write(pickle.dumps(ageList))
    f.close()
    savePath = dataSetFolder + '/genderList.txt'
    f = open(savePath, "wb")
    f.write(pickle.dumps(genderList))
    f.close()
    return imgList, ageList, genderList

def getDataSet(dataSetFolder):
    if os.path.exists(dataSetFolder + '/imgList.txt'):
        print('load data')
        savePath = dataSetFolder + '/imgList.txt'
        with open(savePath, 'rb') as f:
            imgList = pickle.load(f)
        savePath = dataSetFolder + '/ageList.txt'
        with open(savePath, 'rb') as f:
            ageList = pickle.load(f)
        savePath = dataSetFolder + '/genderList.txt'
        with open(savePath, 'rb') as f:
            genderList = pickle.load(f)
    else:
        path = dataSetFolder + '/full_path.txt'
        txtFomat = 'str'
        errorList = []
        imgList = readDataSet(path, txtFomat, errorList)
        path = dataSetFolder + '/dob.txt'
        txtFomat = 'int'
        dobList = readDataSet(path, txtFomat, errorList)
        path = dataSetFolder + '/photo_taken.txt'
        txtFomat = 'int'
        photoTakenList = readDataSet(path, txtFomat, errorList)
        ageList = getAge(errorList, dobList, photoTakenList)
        path = dataSetFolder + '/gender.txt'
        txtFomat = 'int'
        genderList = readDataSet(path, txtFomat, errorList)
        
        faceDetector = detectFaceIF.faceDetector()
        imgList, ageList, genderList = cleanData(dataSetFolder, faceDetector, errorList, imgList, ageList, genderList)
    print('path:', imgList[0], 'age:', ageList[0], 'gender:', genderList[0])
    return imgList, ageList, genderList

if __name__ == "__main__":
    dataSetFolder = 'D:/project/dataSet/imdb/wiki_crop'
    imgList, ageList, genderList = getDataSet(dataSetFolder)
    faceDetector = detectFaceIF.faceDetector()
    ageGenderEstimater = estimateAgeGenderIF.ageGenderEstimater()
    genderStatistician = GenderStatistician()
    ageStatistician = AgeStatistician()
    i = 0
    for imgPath in imgList:
        imagePath = dataSetFolder + '/' + imgPath
        imgColor = cv2.imread(imagePath)
        faces = faceDetector.detectFace(imgColor)
        face = faces[0]
        age, gender = ageGenderEstimater.estimateAgeGender(face)
        # =================================================================================
        cv2.putText(face, age+gender, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 1, cv2.LINE_AA)
        cv2.putText(face, str(ageList[i])+str(genderList[i]), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 1, cv2.LINE_AA)
        cv2.imshow('age', face)
        cv2.waitKey(0)
        # =================================================================================
        if gender == 'Male':
            gender = 1
        else:
            gender = 0
        ageStatistician.judge(int(age), ageList[i], imagePath)
        genderStatistician.judge(gender, genderList[i], imagePath)
        i += 1
        if i == 100:
            break
    ageStatistician.printResult()
    genderStatistician.printResult()
