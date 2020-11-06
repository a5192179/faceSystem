# USAGE
"""
python extract_embeddings.py  --dataset myDataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding_model 20180402-114759.pb
"""
# import the necessary packages
from imutils import paths
import tensorflow as tf
print(tf.__version__)
import numpy as np
import imutils
# import pickle
import cv2
import os
# import sys
# sys.path.append('./module/embedFace/math')
# import distance
from myMath import distance
import shutil
import time
# sys.path.append('./module/embedFace/algo')
# import embedFace
from algo import embedFace


# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
# embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
faceEmbedder = embedFace.faceEmbedder()
# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
dataset = 'D:/project/AiBox/data/debug1102'
imagePaths = list(paths.list_images(dataset))

# initialize our lists of extracted facial embeddings and
# corresponding people names
knownEmbeddings = []
knownNames = []

# initialize the total number of faces processed
total = 0

for (i, imagePath) in enumerate(imagePaths): 
    name = imagePath.split(os.path.sep)[-1]
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
# f = open(args["embeddings"], "wb")
# f.write(pickle.dumps(data))
# f.close()

threshold = 0.245
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
    else:
        identities[newKey] = [newKey]
# save
outDir = '../output'
imgDir = dataset
if outDir != 'null' :
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    else:
        shutil.rmtree(outDir)
        os.mkdir(outDir)
    for key in identities:
        groupDirName = key.split('.')[0]
        groupDir = outDir + '/' + groupDirName
        if not os.path.exists(groupDir):
            os.mkdir(groupDir)
        else:
            shutil.rmtree(groupDir)
            os.mkdir(groupDir)
        for member in identities[key]:
            oriFilePath = imgDir + '/' + member
            newFilePath = groupDir + '/' + member
            shutil.copy(oriFilePath, newFilePath)
    