import numpy as np
import tensorflow as tf
import cv2

class faceEmbedder:
    def __init__(self, ff_pb_path='./module/embedFace/model/20180402-114759.pb'):
        self.graph = tf.get_default_graph()
        self.face_feature_sess = tf.Session()
        with self.face_feature_sess.as_default():
            ff_od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(ff_pb_path, 'rb') as fid:
                serialized_graph = fid.read()
                ff_od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(ff_od_graph_def, name='')
                self.ff_images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                self.ff_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                self.ff_embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")


    def prewhiten(self, x):
        mean = np.mean(x)
        std = np.std(x)
        std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
        y = np.multiply(np.subtract(x, mean), 1/std_adj)
        return y

    def embedFace(self, face):
        """
        docstring
        """
        (fH, fW) = face.shape[:2]
        # ensure the face width and height are sufficiently large
        if fW < 20 or fH < 20:
            vec = []
            return vec
        # construct a blob for the face ROI
        im_data = self.prewhiten(face)
        im_data = cv2.resize(im_data, (160, 160))
        im_data = np.expand_dims(im_data, axis=0)
        vec = self.face_feature_sess.run(self.ff_embeddings,
                                        feed_dict={self.ff_images_placeholder: im_data, self.ff_train_placeholder: False})
        return vec