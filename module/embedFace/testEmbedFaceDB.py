# USAGE
"""
python extract_embeddings.py  --dataset myDataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding_model 20180402-114759.pb
"""
# import the necessary packages
from imutils import paths
import tensorflow as tf
import numpy as np
import imutils
import pickle
import cv2
import os
import sys
sys.path.append('.')
# import sys
# sys.path.append('./module/embedFace/math')
# import distance
from module.embedFace.myMath import distance
import shutil
import time
# sys.path.append('./module/embedFace/algo')
# import embedFace
from module.embedFace.algo import embedFaceIF as embedFace
# from module.embedFace.algo import embedFace
# from common.myPlot import myHist
import matplotlib.pyplot as plt

class Statistician:
    def __init__(self):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.TPPair = []
        self.TNPair = []
        self.FPPair = []
        self.FNPair = []

    def judge(self, predictFlag, str1, str2):
        if str1 == 'null':
            return
        if predictFlag == True:
            if isSame(str1, str2):
                self.TP += 1
                self.TPPair.append(str1 + '_' + str2)
            else:
                self.FP += 1
                self.FPPair.append(str1 + '_' + str2)
        else:
            if isSame(str1, str2):
                self.FN += 1
                self.FNPair.append(str1 + '_' + str2)
            else:
                self.TN += 1
                self.TNPair.append(str1 + '_' + str2)

    def printResult(self):
        print('acc', (self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN))
        A=1

def getImgList(path):
    foldersList = []
    foldersList.append(path)
    imgList = []
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
                    imgList.append(filePath)
                # ==========================
        print(tempRootDir + ' dir end')
        foldersList.pop(0)
    return imgList

def isSame(str1, str2):
    group1 = str1.split('/')[-2]
    group2 = str2.split('/')[-2]
    if group1 == group2:
        return True
    else:
        return False

# outDir = '../output/testEmbedIF'
outDir = 'null'
# imgDir = dataset
if outDir != 'null' :
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    else:
        shutil.rmtree(outDir)
        os.mkdir(outDir)

dataPath = '../data/testFaceIF'
imgList = getImgList(dataPath)
embedPath = dataPath + '/emDict1.txt'

if os.path.exists(embedPath):
    print('load emdict')
    with open(embedPath, 'rb') as f:
        emDict = pickle.load(f)
else:
    # load our serialized face embedding model from disk
    
    print("[INFO] loading face recognizer...")
    # embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
    faceEmbedder = embedFace.faceEmbedder()
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    # initialize our lists of extracted facial embeddings and
    # corresponding people names
    knownEmbeddings = []
    knownNames = []

    # initialize the total number of faces processed
    total = 0
    ts = time.time()
    for imagePath in imgList: 
        name = imagePath
        imgColor = cv2.imread(imagePath)
        # imgGray = cv2.cvtColor(imgColor, cv2.COLOR_BGR2GRAY)
        face = imgColor
        vec = faceEmbedder.embedFace(face)
        # print(vec.shape)
        # print('name', name, 'vec0:', vec[0][0], 'vec-1:', vec[0][-1])
        # add the name of the person + corresponding face
        # embedding to their respective lists
        knownNames.append(name)
        knownEmbeddings.append(vec.flatten())
        total += 1

    # dump the facial embeddings + names to disk
    print("[INFO] serializing {} encodings...".format(total))
    emDict = dict(zip(knownNames, knownEmbeddings))
    # f = open(embedPath, "wb")
    # f.write(pickle.dumps(emDict))
    # f.close()

statistician = Statistician()

threshold = 0.4
identities = {}
for newKey in emDict:
    if len(emDict) == 0:
        identities[newKey] = [newKey]
        continue
    embeddings1 = emDict[newKey]
    bSame = False
    sameKey = 'null'
    nearestDist = 0
    for baseKey in identities:
        embeddings2 = emDict[baseKey]
        dist = distance.distance(embeddings1, embeddings2, 1)
        if dist < threshold:
            if not bSame:
                bSame = True
            if sameKey == 'null':
                sameKey = baseKey
                nearestDist = dist
            elif dist < nearestDist:
                sameKey = baseKey
                nearestDist = dist
    if bSame:
        identities[sameKey].append(newKey)
        statistician.judge(True, sameKey, newKey)
    else:
        identities[newKey] = [newKey]
        statistician.judge(False, sameKey, newKey)
print('deal time(s):', time.time() - ts)
statistician.printResult()
# ==================================
# save
# if outDir != 'null' :
#     for key in identities:
#         groupDirName = key.split('/')[-2] + '-' + key.split('/')[-1].split('.')[-2]
#         groupDir = outDir + '/' + groupDirName
#         if not os.path.exists(groupDir):
#             os.mkdir(groupDir)
#         else:
#             shutil.rmtree(groupDir)
#             os.mkdir(groupDir)
#         for member in identities[key]:
#             oriFilePath = member
#             newFilePath = groupDir + '/' + member.split('/')[-1]
#             shutil.copy(oriFilePath, newFilePath)
# ==================================
# ==================================
# sameList = []
# samePair = []
# diffList = []
# diffPair = []
# compareNum = 0
# resultNum = 0
# for key1 in emDict:
#     embeddings1 = emDict[key1]
#     for key2 in emDict:
#         if key1 == key2:
#             continue
#         compareNum += 1
#         if samePair.count(key2 + '_' + key1) > 0 or diffPair.count(key2 + '_' + key1) > 0:
#             continue
#         embeddings2 = emDict[key2]
#         dist = distance.distance(embeddings1, embeddings2, 1)
#         if isSame(key1, key2):
#             sameList.append(dist)
#             samePair.append(key1 + '_' + key2)
#             resultNum += 1
#         else:
#             diffList.append(dist)
#             diffPair.append(key1 + '_' + key2)
#             resultNum += 1
# print('compareNum:', compareNum, ' resultNum:', resultNum)
# plt.figure()
# plt.hist(sameList)
# plt.grid()
# plt.figure()
# plt.hist(diffList)
# plt.grid()
# plt.show()
# ==================================