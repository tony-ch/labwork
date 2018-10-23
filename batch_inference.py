import os
from options.test_options import TestOptions
from data import CreateDataLoader
from models import create_model
from util.visualizer import save_images
from util import html
from util import util
import os
import ntpath
from scipy.misc import imresize
import shutil
import scipy.io as sio
import cv2

# save image to the disk
def my_save_images(visuals, image_path, aspect_ratio=1.0, width=256):
    image_dir = "./tmp/"
    short_path = ntpath.basename(image_path[0])
    name = os.path.splitext(short_path)[0]

    for label, im_data in visuals.items():
        # only save the A2B result
        if label == "fake_B":
            im = util.tensor2im(im_data)
            image_name = '%s_%s.png' % (name, label)
            save_path = os.path.join(image_dir, image_name)
            h, w, _ = im.shape
            if aspect_ratio > 1.0:
                im = imresize(im, (h, int(w * aspect_ratio)), interp='bicubic')
            if aspect_ratio < 1.0:
                im = imresize(im, (int(h / aspect_ratio), w), interp='bicubic')
            util.save_image(im, save_path)
    return save_path


def my_create_model():
    opt = TestOptions().parse()
    # hard-code some parameters for test
    opt.num_threads = 1   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True    # no flip
    opt.display_id = -1   # no visdom display

    opt.name = "shape02shape1_noflip_cyclegan"  # model checkpoint saved
    opt.model = "cycle_gan"
    opt.phase = "test"
    opt.no_dropout = True
    opt.dataset_mode = "unaligned"
    opt.dataroot = "./tmp"

    model = create_model(opt)
    model.setup(opt)
    return opt, model


def my_inference(model, opt, img_path):
    print (img_path)
    assert(os.path.exists(img_path) and os.path.isfile(img_path))
    A_dir = "./tmp/testA"
    B_dir = "./tmp/testB"

    if os.path.exists(A_dir):
        shutil.rmtree(A_dir)
    if os.path.exists(B_dir):
        shutil.rmtree(B_dir)
    os.makedirs(A_dir)
    os.makedirs(B_dir)

    img_name = os.path.basename(img_path)
    des1 = os.path.join(A_dir, img_name)
    des2 = os.path.join(B_dir, img_name)
    shutil.copyfile(img_path, des1)
    shutil.copyfile(img_path, des2)

    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()

    for i, data in enumerate(dataset):
        model.set_input(data)
        model.test()
        visuals = model.get_current_visuals()
        img_path = model.get_image_paths()
        save_path = my_save_images(visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
        break  # only test one image
    return save_path


def my_batch_inference(model, opt, img_path):
    ###input :  M*N*3*256
    print (img_path)


    assert(os.path.exists(img_path) and os.path.isfile(img_path))
    A_dir = "./tmp/testA"
    B_dir = "./tmp/testB"

    if os.path.exists(A_dir):
        shutil.rmtree(A_dir)
    if os.path.exists(B_dir):
        shutil.rmtree(B_dir)
    os.makedirs(A_dir)
    os.makedirs(B_dir)
    batchdata= sio.loadmat(img_path)['batch']
    orisize=batchdata.shape[0]
    for i in range(0,batchdata.shape[3]):
        img = batchdata[:,:,:,i]
        cv2.imwrite(os.path.join(A_dir,str(i)+".jpg"),img)
        cv2.imwrite(os.path.join(B_dir,str(i)+".jpg"),img)

    img_name = os.path.basename(img_path)
    des1 = os.path.join(A_dir, img_name)
    des2 = os.path.join(B_dir, img_name)
    shutil.copyfile(img_path, des1)
    shutil.copyfile(img_path, des2)

    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()

    imgnamelist=[]
    for i, data in enumerate(dataset):
        model.set_input(data)
        model.test()
        visuals = model.get_current_visuals()
        img_path = model.get_image_paths()
        save_path = my_save_images(visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
        imgnamelist.append(save_path)
        # imgdict['name']=save_path
        # break  # only test one image
    x_data=[]
    for img in imgnamelist:
        image = cv2.imread(img)
        image = cv2.resize(image,(orisize, orisize))
        x_data.append (image)
    save_path = 'temp/batch.mat'
    sio.savemat(save_path,{'batch':x_data})


    return save_path

if __name__ == '__main__':
    # build the model
    opt, model = my_create_model()

    # change the image path for inference , return save path
    # img_path = "/data3/liuliang/data/shapenet01_few/0/22032.png"
    # save_path = my_inference(model, opt, img_path)
    # print(save_path)
    batch_path = "/home/swf/swfcode/matlab/Vital_release-master/tracking/batch.mat"
    save_path = my_batch_inference(model, opt, batch_path)
    print(save_path)

