import sys
sys.path.append('.')
from module.verifyFace.algo import verifyFace
import cv2

faceVerifier = verifyFace.faceVerifier()

imagePath = 'D:/project/touristAnalyse/data/good-small/14.jpg'
imgColor = cv2.imread(imagePath)
bInBase, identity, age, gender = faceVerifier.verifyFace(imgColor)
print('bInBase:', bInBase, 'identity:', identity, 'age:', age, 'gender:', gender)