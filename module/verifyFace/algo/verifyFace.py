# from module.embedFace.algo import embedFace
from module.embedFace.algo import embedFaceIF as embedFace
from module.embedFace.myMath import distance
# from module.estimateAgeGender.algo import estimateAgeGender
from module.estimateAgeGender.algo import estimateAgeGenderIF as estimateAgeGender
import json
from collections import OrderedDict
import numpy as np
import datetime
import os

# input a img, output whether is in facebase
class faceVerifier:
    def __init__(self, identityBase, similarThreshold = 0.245, ageScale = 1.0, useGPU = False):
        # if os.path.exists(dataPath):
        #     f = open(dataPath)
        #     content = f.read()
        #     self.facebase = json.loads(content, object_pairs_hook=OrderedDict)
        # else:
        #     self.facebase = {}
        # print('load facebase end, num:', len(self.facebase))
        self.identityBase = identityBase
        self.faceEmbedder = embedFace.faceEmbedder(useGPU = useGPU)
        self.ageGenderEstimater = estimateAgeGender.ageGenderEstimater(ageScale = ageScale, useGPU = useGPU)
        self.similarThreshold = similarThreshold

    def insert(self, face, vec):
        pass

    def search(self, face, vec):
        minDist = -1
        minIdentity = 'null'
        secondDist = -1
        secondIdentity = 'null'
        for identity in self.identityBase.keys():
            if identity == 'nextId':
                continue
            dist = distance.distance(vec, np.array(self.identityBase[identity]['vec']), 1)
            if minDist < 0 or minDist > dist:
                minDist = dist
                minIdentity = identity
            if secondDist < 0 or (minDist < dist and secondDist > dist):
                secondDist = dist
                secondIdentity = identity
        # print('minIdentity:', minIdentity, 'minDist:', minDist)
        if minDist >= 0 and minDist < self.similarThreshold:
            if secondDist < self.similarThreshold * 0.8 and secondIdentity != minIdentity:
                deleteID = str(max(int(secondIdentity), int(minIdentity)))
                del self.identityBase[deleteID]
                print('combine,', minIdentity, ',', secondIdentity, ',delete', deleteID, )
                minIdentity = str(min(int(secondIdentity), int(minIdentity)))
            bInBase = True
            identity = minIdentity
            age = self.identityBase[identity]['age']
            gender = self.identityBase[identity]['gender']
        else:
            # identityBase insert
            bInBase = False
            identity = str(self.identityBase['nextId'])
            self.identityBase['nextId'] = self.identityBase['nextId'] + 1
            age, gender = self.ageGenderEstimater.estimateAgeGender(face)
            img = 'new'
            timeInfo = {}
            person = {'age':age, 'gender':gender, 'img':img, 'vec':vec.tolist(), 'timeInfo':timeInfo}
            self.identityBase[identity] = person
        return bInBase, identity, age, gender

    def verifyFace(self, face):
        vec = self.faceEmbedder.embedFace(face).flatten()
        bInBase, identity, age, gender = self.search(face, vec)
        return bInBase, identity, age, gender

    def saveFacebase(self, savaFolder = '../data/identityBase'):
        timeStr = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")
        jsonPath = savaFolder + '/identityBase' + timeStr + '.json'
        f=open(jsonPath,'a',encoding='utf-8')
        json.dump(self.identityBase, f, indent=2)

    def verifyFaces(self, faces):
        bInBases = []
        identities = []
        ages = []
        genders = []
        for face in faces:
            bInBase, identity, age, gender = self.verifyFace(face)
            bInBases.append(bInBase)
            identities.append(identity)
            ages.append(age)
            genders.append(gender)
        return bInBases, identities, ages, genders

    def getAgeAndGender(self, identity):
        if not identity in self.identityBase.keys():
            print(identity, 'is not in identityBase!')
            return []
        return self.identityBase[identity]['age'], self.identityBase[identity]['gender']