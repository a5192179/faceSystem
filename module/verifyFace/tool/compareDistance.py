import sys
sys.path.append('.')
import cv2
from module.embedFace.algo import embedFace
from module.embedFace.myMath import distance
import json

faceEmbedder = embedFace.faceEmbedder()

imagePath1 = 'D:/project/touristAnalyse/data/good-small/13.jpg'
imagePath2 = 'D:/project/touristAnalyse/data/good-small/14.jpg'
face1 = cv2.imread(imagePath1)
face2 = cv2.imread(imagePath2)

vec1 = faceEmbedder.embedFace(face1).flatten()
vec2 = faceEmbedder.embedFace(face2).flatten()
dist = distance.distance(vec1, vec2, 1)
print('distance', dist, ' ', imagePath1, ' ', imagePath2)

vj = {}
vj['img1'] = vec1.tolist()
vj['img2'] = vec2.tolist()
jsonPath = '../output/vj.json'
f=open(jsonPath,'w',encoding='utf-8')
json.dump(vj, f, indent=2) # indent 缩进控制