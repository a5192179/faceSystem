libs = []
# keras==2.1.0
import numpy as np
import cv2
import sys
sys.path.append('.')
from module.estimateAgeGender.util.SSR_model import SSR_net
import module.estimateAgeGender.util.Main_yolo as My
from module.estimateAgeGender.util.ageLabel import age_label
import tensorflow as tf
try:
    libs.append('tensorflow==' + tf.__version__ + '\n')
except:
    libs.append('tensorflow' + '\n')
from PIL import Image
import PIL
try:
    libs.append('PIL==' + PIL.__version__ + '\n')
except:
    libs.append('PIL' + '\n')
import os
# =============================
txtPath = './dependence.txt'
with open(txtPath, "a") as f:
    for line in libs:
        f.write(line)
# =============================

class ageGenderEstimater:
    def __init__(self, ageScale = 1.0, modelFile = './module/estimateAgeGender/model/ssrnet_3_3_3_64_1.0_1.0.h5', pb_path_sex = "./module/estimateAgeGender/model/face_attribute.pb"):
        self.model = SSR_net()()
        self.model.load_weights(modelFile)
        self.graph = tf.get_default_graph()
        self.detection_sess = tf.Session()
        self.pred_eyegalsses, self.pred_male = My.model_sex(self.detection_sess, pb_path_sex)
        self.ageScale = ageScale

    def estimateAgeGenderbyArray(self, imgArray):
        # cv2.imshow('img', imgArray)
        # waitkey(0)
        im_data_age = cv2.resize(imgArray, (64, 64))
        age_p = self.model.predict(np.expand_dims(im_data_age, 0))
        pred_age = int(age_p[0][0] * self.ageScale)
        if pred_age < 18:
            pred_age += 5
        age = age_label(pred_age)
        
        # sex
        im_data_sex = cv2.resize(imgArray, (128, 128))
        eye, sex = self.detection_sess.run([self.pred_eyegalsses, self.pred_male],
                                        feed_dict={"Placeholder_96:0": np.expand_dims(im_data_sex, 0)})
        if sex[0] == 1:
            gender = "Male"
        else:
            gender = "Female"
        # display_str_list = My.display(eye, sex, age)
        # imageCv = My.draw_attr(imageCv, y1, x1, y2, x2, display_str_list)
        # print(imageCv.shape)
        # print(display_str_list)
        # cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('img', imageCv)
        # cv2.waitKey(0)
        return age, gender

