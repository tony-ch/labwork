#!/usr/bin/env python
#-*- coding:utf-8 -*-

#@title Imports

import os
import time

from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

import tensorflow as tf

class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph.pb'

    def __init__(self, model_path):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        graph_path = os.path.join(model_path, self.FROZEN_GRAPH_NAME)
        with tf.gfile.FastGFile(graph_path,'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
            image: A PIL.Image object, raw input image.

        Returns:
            #resized_image: RGB image resized from original input image.
            seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
                self.OUTPUT_TENSOR_NAME,
                feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        #seg_map = np.resize(seg_map,(height,width))
        return image, seg_map

def create_model():
    sstime=time.time()
    opt={}
    opt['model_dir']="models/deeplabv3/"
    opt['save_dir']='../result/'
    opt['suffix']='.jpg'
    print('loading DeepLab model...')

    MODEL = DeepLabModel(opt['model_dir'])
    print('model loaded successfully!')
    etime=time.time()
    print(etime-sstime)
    return opt, MODEL

def batch_inference(MODEL, opt, path):
    try:
        orignal_im = Image.open(path)
        # orignal_im = handle_orientation(orignal_im)
        # plt.imshow(orignal_im)
        # plt.show()
    except IOError:
        print('Cannot retrieve image. Please check url: ' + path)
        return

    print('running deeplab on image %s...' % path)

    resized_im, seg_map = MODEL.run(orignal_im)
    # seg_map[seg_map<0.5]=0
    # seg_map[seg_map>=0.5]=1
    seg_map = seg_map * 255
    width,height = orignal_im.size
    size = (width,height)
    trimap_image = Image.fromarray(seg_map.astype(dtype=np.uint8))
    trimap_image = trimap_image.resize(size)

    file_name = os.path.basename(path)[:-4]+opt['suffix']

    #if not os.path.isabs(path):#图片列表给出的项目是相对img_root的路径
    #    file_name=path[:-4]
    #    tf.gfile.MakeDirs(os.path.dirname(opt['save_dir']+"/"+path))
    save_dir = os.path.abspath(opt['save_dir'])
    if not os.path.exists(save_dir):
        tf.gfile.MakeDirs(save_dir)
    save_path = os.path.join(save_dir,file_name)
    with tf.gfile.Open(save_path , mode='w') as f:
        trimap_image.save(f, 'JPEG')

    return save_path