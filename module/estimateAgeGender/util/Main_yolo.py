libs = []
import tensorflow as tf
import numpy as np
import colorsys, cv2, os
# try:
#     libs.append('colorsys==' + colorsys.__version__ + '\n')
# except:
#     libs.append('colorsys' + '\n')
from timeit import default_timer as timer
from PIL import Image, ImageFont, ImageDraw
from keras import backend as K
import keras
try:
    libs.append('keras==' + keras.__version__ + '\n')
except:
    libs.append('keras' + '\n')
from keras.layers import Input
from module.estimateAgeGender.util.yolo3.model import yolo_eval, yolo_body
from module.estimateAgeGender.util.yolo3.utils import letterbox_image

# =============================
txtPath = './dependence.txt'
with open(txtPath, "a") as f:
    for line in libs:
        f.write(line)
# =============================
class YOLO(object):
    def __init__(self):
        self.anchors_path = os.path.join('./module/estimateAgeGender/configs/yolo_anchors.txt')  # Anchors
        #self.model_path = 'model_data/yolo_weights.h5'  # 模型文件
        #self.classes_path = 'configs/coco_classes_ch.txt'  # 类别文件
        self.model_path = os.path.join('./module/estimateAgeGender/model/ep062-loss28.215-val_loss28.491.h5')  # 模型文件
        self.classes_path = os.path.join('./module/estimateAgeGender/configs/wider_classes.txt')  # 类别文件
        self.score = 0.50  # 0.6
        self.iou = 0.45
        # self.iou = 0.01
        self.class_names = self._get_class()  # 获取类别
        self.anchors = self._get_anchors()  # 获取anchor
        self.sess = K.get_session()
        self.model_image_size = (416, 416)  # fixed size or (None, None), hw
        self.colors = self.__get_colors(self.class_names)
        self.boxes, self.scores, self.classes = self.generate()

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path, encoding='utf8') as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    @staticmethod
    def __get_colors(names):
        # 不同的框，不同的颜色
        hsv_tuples = [(float(x) / len(names), 1., 1.)
                      for x in range(len(names))]  # 不同颜色
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))  # RGB
        np.random.seed(10101)
        np.random.shuffle(colors)
        np.random.seed(None)
        return colors

    def generate(self):
        model_path = os.path.expanduser(self.model_path)  # 转换~
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'
        num_anchors = len(self.anchors)  # anchors的数量
        num_classes = len(self.class_names)  # 类别数
        self.yolo_model = yolo_body(Input(shape=(416, 416, 3)), 3, num_classes)
        self.yolo_model.load_weights(model_path)  # 加载模型参数
        print('{} model, {} anchors, and {} classes loaded.'.format(model_path, num_anchors, num_classes))
        # 根据检测参数，过滤框
        self.input_image_shape = K.placeholder(shape=(2,))
        boxes, scores, classes = yolo_eval(
            self.yolo_model.output, self.anchors, len(self.class_names),
            self.input_image_shape, score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes

    def detect_image(self, image):
        start = timer()  # 起始时间
        if self.model_image_size != (None, None):  # 416x416, 416=32*13，必须为32的倍数，最小尺度是除以32
            assert self.model_image_size[0] % 32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1] % 32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))  # 填充图像
        else:
            new_image_size = (image.width - (image.width % 32), image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')
        # print('detector size {}'.format(image_data.shape))
        image_data /= 255.  # 转换0~1
        image_data = np.expand_dims(image_data, 0)  # 添加批次维度，将图片增加1维
        # 参数盒子、得分、类别；输入图像0~1，4维；原始图像的尺寸
        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        end = timer()
        print(end - start)  # 检测执行时间
        return out_boxes, out_scores, out_classes

    def detect_objects_of_image(self, img_path):
        image = Image.open(img_path)
        assert self.model_image_size[0] % 32 == 0, 'Multiples of 32 required'
        assert self.model_image_size[1] % 32 == 0, 'Multiples of 32 required'
        boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))  # 填充图像
        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.  # 转换0~1
        image_data = np.expand_dims(image_data, 0)  # 添加批次维度，将图片增加1维
        # print('detector size {}'.format(image_data.shape))
        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        img_size = image.size[0] * image.size[1]
        objects_line = self._filter_boxes(out_boxes, out_scores, out_classes, img_size)
        return objects_line

    def _filter_boxes(self, boxes, scores, classes, img_size):
        res_items = []
        for box, score, clazz in zip(boxes, scores, classes):
            top, left, bottom, right = box
            box_size = (bottom - top) * (right - left)
            rate = float(box_size) / float(img_size)
            clz_name = self.class_names[clazz]
            if rate > 0.05:
                res_items.append('{}-{:0.2f}'.format(clz_name, rate))
        res_line = ','.join(res_items)
        return res_line

    def close_session(self):
        self.sess.close()


def draw_attr(image, top, left, bottom, right, display_str_list):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Times.ttc', 12)
    except IOError:
        font = ImageFont.load_default()
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=4, fill="green")
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    display_str_width = [font.getsize(ds)[0] for ds in display_str_list]
    text_width_most = max(display_str_width)
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)
    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = bottom + total_display_str_height
    for display_str in display_str_list[::-1]:
        _, text_height = font.getsize(display_str)
        draw.rectangle(
            [(left, text_bottom - text_height), (left + text_width_most, text_bottom)],
            fill='green')
        draw.text(
            (left, text_bottom - text_height),
            display_str,
            fill='black',
            font=font)
        text_bottom -= text_height
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def display(eye, sex, age):
    if sex[0] == 1:
        gender = "Male"
    else:
        gender = "Female"
    if eye[0] == 1:
        glasses = "Yes"
    else:
        glasses = "No"
    display_str_list = ['Gender: {}'.format(gender), 'Age: {}'.format(age), 'Eyeglasses: {}'.format(glasses)]
    return display_str_list


def model_age(detection_sess, pb_path_age):
    with detection_sess.as_default():
        # tf.reset_default_graph()
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(pb_path_age, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
            # graph = tf.get_default_graph()
            # for op in graph.get_operations():
            #     print(op.name)
    pred_age = detection_sess.graph.get_tensor_by_name("dense_2/BiasAdd:0")
    # pred_age = detection_sess.graph.get_tensor_by_name("ArgMax:0")
    return pred_age


def model_sex(detection_sess, pb_path_sex):
    with detection_sess.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(pb_path_sex, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    pred_eyegalsses = detection_sess.graph.get_tensor_by_name("ArgMax:0")
    pred_male = detection_sess.graph.get_tensor_by_name("ArgMax_2:0")
    placeholder = detection_sess.graph.get_tensor_by_name("Placeholder:0")
    print(placeholder.shape)
    return pred_eyegalsses, pred_male


# if __name__ == "__main__":
#     img_path = 'C:/Users/44618/Pictures/test/image2.jpg'
#     # img_path = 'D:/Program/PycharmProjects/DLearning/AgeInference_yolo/dataset/4.jpg'
#     # img_path = 'C:/Users/44618/Pictures/test/image5.jpg'
#     pb_path_age = "D:/Program/PycharmProjects/DLearning/AgeInference_yolo/pb/age_attribute.pb"
#     # # pb_path_age = "D:\\Program\\PycharmProjects\\DLearning\\Age-identification\\model\\face_attribute_inception_pro.pb"
#     # pb_path_age = "D:\\Program\\PycharmProjects\\DLearning\\Age-identification\\model\\age_attribute.pb"
#     pb_path_sex = "D:/Program/PycharmProjects/DLearning/AgeInference_yolo/pb/face_attribute.pb"
#     basePath = 'D:/Program/PycharmProjects/DLearning/AgeInference_yolo'
#     classes = ['baby', 'teenager', 'younger', 'adult', 'older']
#     detection_sess = tf.Session()
#     pred_age = model_age(detection_sess, pb_path_age)
#     pred_eyegalsses, pred_male = model_sex(detection_sess, pb_path_sex)
#     yolo = YOLO()
#     imageCv = cv2.imread(img_path)
#     image = Image.fromarray(cv2.cvtColor(imageCv, cv2.COLOR_BGR2RGB))
#     out_boxes, out_scores, out_classes = yolo.detect_image(image)
#     # print(out_boxes, out_scores, out_classes)
#     for i in range(len(out_scores)):
#         if out_scores[i] >= 0.5:
#             top, left, bottom, right = out_boxes[i]
#             top, left, bottom, right = int(top), int(left), int(bottom), int(right)
#             # print(top, left, bottom, right)
#             image_data = imageCv[top:bottom, left:right]
#             im_data = cv2.resize(image_data, (128, 128))
#             # print(np.expand_dims(im_data, 0).shape)
#             im_data = np.array(im_data, dtype="float32")
#             # print(im_data.dtype)
#             logits = detection_sess.run([pred_age], feed_dict={"x:0": np.expand_dims(im_data, 0)})
#             eye, sex = detection_sess.run([pred_eyegalsses, pred_male],
#                                           feed_dict={"Placeholder:0": np.expand_dims(im_data, 0)})
#
#             num = np.argmax(logits)
#             age = classes[int(num)]
#             # age = classes[logits[0]]
#             display_str_list = display(eye, sex, age)
#             imageCv = draw_attr(imageCv, top, left, bottom, right, display_str_list)
#             print(imageCv.shape)
#             print(display_str_list)
#     cv2.imshow('111', imageCv)
#     cv2.waitKey(0)


