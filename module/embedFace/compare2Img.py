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
face1 = cv2.imread('../output/ISCameraLS_000003/face/336-0.jpg')
vec1 = faceEmbedder.embedFace(face1).flatten()
face2 = cv2.imread('../output/ISCameraLS_000003/face/24-0.jpg')
vec2 = faceEmbedder.embedFace(face2).flatten()

dist = distance.distance(vec1, vec2, 1)
print(dist)

    