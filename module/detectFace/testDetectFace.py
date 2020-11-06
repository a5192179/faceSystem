from algo import detectFace
import cv2
from imutils import paths

faceDetector = detectFace.faceDetector()
dataset = 'D:/project/faceDetect/data/holeImage'
imagePaths = list(paths.list_images(dataset))
for (i, imagePath) in enumerate(imagePaths):
    imgColor = cv2.imread(imagePath)
    faceDetector.detectFace(imgColor)
    