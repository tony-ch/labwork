#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import print_function
from rasl import rasl
from rasl.application import load_images
from rasl.application import rasl_arg_parser
from rasl.tform import EuclideanTransform, SimilarityTransform, AffineTransform, ProjectiveTransform

import numpy as np
from matplotlib import pyplot as plt
from argparse import ArgumentParser
import os,shutil
from PIL import Image
import cv2 as cv

def remove_margin(im):
    x,y = im.shape

    zero_ind = (im <= 10)
    x_sum = np.sum(zero_ind,axis=1)
    y_sum = np.sum(zero_ind,axis=0)
    for xl in range(x):
        if x_sum[xl]<y/2:
            break
    for yl in range(y):
        if y_sum[yl]<x/2:
            break
    for xh in range(x,1,-1):
        if x_sum[xh-1]<y/2:
            break
    for yh in range(y,1,-1):
        if y_sum[yh-1]<x/2:
            break
    print(" crop at (%d,%d,%d,%d)"%(xl,xh,yl,yh))
    return im[xl:xh, yl:yh]

def run_subdir(description="load and align images in a directory",
             path=None, frame=0, grid=(2,2), tform=AffineTransform, save_dir=None):
    parser = rasl_arg_parser(description=description, path=path, frame=frame,
                             grid=grid, tform=tform)
    args = parser.parse_args()
    images = load_images(args.path)
    shapes = np.array([image.shape for image in images])
    new_shape=(np.min(shapes[:, 0]), np.min(shapes[:, 1]))
    images = [cv.resize(im,(100,100),interpolation=cv.INTER_CUBIC) for im in images]
    print("resize to (%d,%d)"%(new_shape[1],new_shape[0]))

    if len(images) < np.prod(args.grid):
        raise ValueError("Only {} images, specify a smaller --grid than {}"\
                         .format(len(images), args.grid))
    T = [args.tform().inset(image.shape, args.frame)
         for image in images]
    """
    L : array(nimages) of ndarray(h, v)
        aligned low-rank images
    S : array(nimages) of ndarray(h, v)
        aligned sparse error images
    T : array(nimages) of TForm
        final transforms. Each will include initT's inset frame and
        the aligning paramv
    iter : int
        number of iterations to convergence
    """
   
    # L, S, T, itr = rasl(images, T, stop_delta=args.stop, show=args.grid)
    # for j in range(len(L)):
    #     im = Image.fromarray((L[j]/np.max(L[j])*255).astype(np.uint8))
    #     im.save(os.path.join(save_dir,"%04d.png"%(j)))
    # print("click the image to exit")
    # plt.waitforbuttonpress()
    for i in range(0,len(images),40):
        end= i+40 if i+40 <= len(images) else len(images)
        if i == 120:
            print('this is ')
        print("begin %d, end %d"%(i,end))
        L, S, T, itr = rasl(images[i:end], T, stop_delta=args.stop*10, show=None)
        for j in range(len(L)):
            im = (L[j]-np.min(L[j]))/(np.max(L[j])-np.min(L[j]))*255
            #plt.imshow(im)
            #plt.show()
            im = remove_margin(im)
            #plt.imshow(im)
            #plt.show()
            im = cv.resize(im, (shapes[i+j][1],shapes[i+j][0]),interpolation=cv.INTER_CUBIC)
            im = Image.fromarray(im.astype(np.uint8))
            im.save(os.path.join(save_dir,"%04d.png"%(i+j)))
        #print("click the image to exit")
        #plt.waitforbuttonpress()

def run_all(path, save_dir):
    print("run in %s\n save res in %s\n"% (path,save_dir))
    os.makedirs(save_dir)
    dirs = [ d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d)) ]
    for d in dirs:
        run_all(os.path.join(path,d),os.path.join(save_dir,d))
    
    if len(dirs)>0:
        return
    run_subdir(path=path, save_dir=save_dir)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--path', default='./data/test/', help='img dir to run demo')
    parser.add_argument('--save_dir', default='./res/res_s40_stop0.05_resize_100x100_crop/', help='dir to save res')
    args = parser.parse_args()
    shutil.rmtree(args.save_dir,ignore_errors=True)
    run_all(args.path, args.save_dir)