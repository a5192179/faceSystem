from module.embedFace.algo import embedFace
from module.embedFace.myMath import distance
# from module.estimateAgeGender.algo import estimateAgeGender
from module.estimateAgeGender.algo import estimateAgeGenderIS as estimateAgeGender
import json
from collections import OrderedDict
import numpy as np
import datetime
import os

# input a img, output whether is in facebase
class faceVerifier:
    def __init__(self, dataPath = '../data/facebase-good-small.json', similarThreshold = 0.245, ageScale = 1.0):
        if os.path.exists(dataPath):
            f = open(dataPath)
            content = f.read()
            self.facebase = json.loads(content, object_pairs_hook=OrderedDict)
        else:
            self.facebase = {}
        print('load facebase end, num:', len(self.facebase))
        self.faceEmbedder = embedFace.faceEmbedder()
        self.ageGenderEstimater = estimateAgeGender.ageGenderEstimater(ageScale = ageScale)
        self.similarThreshold = similarThreshold

    def insert(self, face, vec):
        pass

    def search(self, face, vec):
        minDist = -1
        minIdentity = 'null'
        for identity in self.facebase:
            if identity == 'nextId':
                continue
            dist = distance.distance(vec, np.array(self.facebase[identity]['vec']), 1)
            if minDist < 0 or minDist > dist:
                minDist = dist
                minIdentity = identity
        print('minIdentity:', minIdentity, 'minDist:', minDist)
        if minDist < self.similarThreshold:
            bInBase = True
            identity = minIdentity
            age = self.facebase[identity]['age']
            gender = self.facebase[identity]['gender']
        else:
            bInBase = False
            identity = str(self.facebase['nextId'])
            self.facebase['nextId'] = self.facebase['nextId'] + 1
            age, gender = self.ageGenderEstimater.estimateAgeGender(face)
            img = 'new'
            person = {'age':age, 'gender':gender, 'img':img, 'vec':vec.tolist()}
            self.facebase[identity] = person
        return bInBase, identity, age, gender

    def verifyFace(self, face):
        vec = self.faceEmbedder.embedFace(face).flatten()
        bInBase, identity, age, gender = self.search(face, vec)
        return bInBase, identity, age, gender

    def saveFacebase(self, savaFolder = '../data/facebase'):
        timeStr = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")
        jsonPath = savaFolder + '/facebase' + timeStr + '.json'
        f=open(jsonPath,'a',encoding='utf-8')
        json.dump(self.faceBase, f, indent=2)

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
        if not identity in self.facebase:
            print(identity, 'is not in facebase!')
            return []
        return self.facebase[identity]['age'], self.facebase[identity]['gender']