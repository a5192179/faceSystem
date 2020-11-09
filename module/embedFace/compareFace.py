# USAGE
"""
python extract_embeddings.py  --dataset myDataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding_model 20180402-114759.pb
"""
# import the necessary packages
from imutils import paths
import tensorflow as tf
print(tf.__version__)
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
import sys
sys.path.append('./math')
import distance
import shutil
import time
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
                help="path to input directory of faces + images")
ap.add_argument("-e", "--embeddings", required=True,
                help="path to output serialized db of facial embeddings")
ap.add_argument("-d", "--detector", required=True,
                help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding_model", required=True,
                help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
ap.add_argument("-o", "--output", type=str, default='null',
                help="ouput dir")
args = vars(ap.parse_args())


# 图像数据标准化
def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
# embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
face_feature_sess = tf.Session()
ff_pb_path = args["embedding_model"]
with face_feature_sess.as_default():
    ff_od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(ff_pb_path, 'rb') as fid:
        serialized_graph = fid.read()
        ff_od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(ff_od_graph_def, name='')
        ff_images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        ff_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        ff_embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

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
    ts = time.time()

    (fH, fW) = face.shape[:2]

    # ensure the face width and height are sufficiently large
    if fW < 20 or fH < 20:
        continue

    # construct a blob for the face ROI
    im_data = prewhiten(face)
    im_data = cv2.resize(im_data, (160, 160))
    im_data = np.expand_dims(im_data, axis=0)
    vec = face_feature_sess.run(ff_embeddings,
                                feed_dict={ff_images_placeholder: im_data,
                                            ff_train_placeholder: False})
    print(vec.shape)
    print('name', name, 'vec0:', vec[0][0], 'vec-1:', vec[0][-1])
    # print('time:', time.time() - ts)
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
outDir = args["output"]
imgDir = args["dataset"]
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
    