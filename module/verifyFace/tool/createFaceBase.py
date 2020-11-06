import sys
sys.path.append('.')
from module.embedFace.algo import embedFace
from module.embedFace.myMath import distance
from module.estimateAgeGender.algo import estimateAgeGender
import cv2
from imutils import paths
import os
import json

def getBestVecFromDict(keyList, vecDict):
    if len(keyList) == 1:
        return keyList[0]
    vecs = []
    bestKey = ''
    minDist = 0
    for key in keyList:
        vecs.append(vecDict[key])
    imgNum = len(vecs)
    for i in range(imgNum):
        vecBase = vecs[i]
        distances = 0
        for j in range(imgNum):
            if i == j:
                continue
            vecsNew = vecs[j]
            dist = distance.distance(vecBase, vecsNew)
            distances += dist
        if minDist == 0:
            minDist = distances
            bestKey = keyList[i]
        elif minDist > distances:
            minDist = distances
            bestKey = keyList[i]
    return bestKey
    
if __name__ == "__main__":
    # load our serialized face embedding model from disk
    print("[INFO] loading face recognizer...")
    # embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
    faceEmbedder = embedFace.faceEmbedder()
    ageGenderEstimater = estimateAgeGender.ageGenderEstimater()
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    # dataset = 'D:/project/AiBox/data/debug1102'
    dataset = 'D:/project/touristAnalyse/data/good-small'
    imagePaths = list(paths.list_images(dataset))

    total = 0
    knownEmbeddings = []
    knownNames = []
    ages = []
    genders = []
    for (i, imagePath) in enumerate(imagePaths): 
        name = imagePath.split(os.path.sep)[-1]
        imgColor = cv2.imread(imagePath)
        # imgGray = cv2.cvtColor(imgColor, cv2.COLOR_BGR2GRAY)
        face = imgColor
        vec = faceEmbedder.embedFace(face)
        age, gender = ageGenderEstimater.estimateAgeGenderbyArray(face)
        # print(vec.shape)
        # print('name', name, 'vec0:', vec[0][0], 'vec-1:', vec[0][-1])
        # add the name of the person + corresponding face
        # embedding to their respective lists
        knownNames.append(name)
        knownEmbeddings.append(vec.flatten())
        ages.append(age)
        genders.append(gender)
        total += 1

    # dump the facial embeddings + names to disk
    print("[INFO] serializing {} encodings...".format(total))
    emDict = dict(zip(knownNames, knownEmbeddings))
    ageDict = dict(zip(knownNames, ages))
    genderDict = dict(zip(knownNames, genders))
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
    # save to json
    identity = 0
    faceBase = {}
    for key in identities:
        bestOne = getBestVecFromDict(identities[key], emDict)
        age = ageDict[bestOne]
        gender = genderDict[bestOne]
        vec = emDict[bestOne]
        person = {'age':age, 'gender':gender, 'img':bestOne, 'vec':vec.ravel().tolist()}
        faceBase[str(identity)] = person
        identity = identity + 1
    faceBase['nextId'] = identity
    jsonPath = '../output/facebase-good-small.json'
    f=open(jsonPath,'a',encoding='utf-8')
    json.dump(faceBase, f, indent=2) # indent 缩进控制
