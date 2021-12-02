# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 16:01:13 2019

@author: fonollosa (Berlin)
"""
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

from utils_my import Read_Img_2_Tensor, Load_DeepFashion2_Yolov3, Draw_Bounding_Box
from tensorflow.python.ops.gen_array_ops import empty
import os
import pandas as pd
import scipy.cluster
import scipy.misc
import scipy
from PIL import Image
import struct
import binascii
import sys
import cv2
import tensorflow as tf
import time
import numpy as np



def Detect_Clothes(img, model_yolov3, eager_execution=True):
    """Detect clothes in an image using Yolo-v3 model trained on DeepFashion2 dataset"""
    img = tf.image.resize(img, (416, 416))

    t1 = time.time()
    if eager_execution == True:
        boxes, scores, classes, nums = model_yolov3(img)
        # change eager tensor to numpy array
        boxes, scores, classes, nums = boxes.numpy(
        ), scores.numpy(), classes.numpy(), nums.numpy()
    else:
        boxes, scores, classes, nums = model_yolov3.predict(img)
    t2 = time.time()
    print('Yolo-v3 feed forward: {:.2f} sec'.format(t2 - t1))

    print('detecting clothes...')

    class_names = ['camiseta_manga_corta', 'jersey', 'abrigo_manga_corta', 'abrigo_manga_larga',
                   'chaleco', 'top_tirantes_finos', 'pantalon_corto', 'pantalones', 'falda', 'vestido_manga_corta',
                   'vestido_manga_larga', 'vestido_de_chaleco', 'vestido_tirantes']

    # Parse tensor
    list_obj = []
    for i in range(nums[0]):
        obj = {'label': class_names[int(
            classes[0][i])], 'confidence': scores[0][i]}
        obj['x1'] = boxes[0][i][0]
        obj['y1'] = boxes[0][i][1]
        obj['x2'] = boxes[0][i][2]
        obj['y2'] = boxes[0][i][3]
        list_obj.append(obj)

    return list_obj


def Detect_Color(img_crop):
    # #if the detection's confindence is not above the threshold: 'N/A'
    # if img_crop is None:
    #     return 'N/A'

    NUM_CLUSTERS = 5

    print('detecting color...', end=' ')
    im = img_crop
    im = Image.fromarray((im * 255).astype(np.uint8))

    im = im.resize((150, 150))      # optional, to reduce time
    #chroma = np.array([0, 177, 64], dtype=np.uint8)
    ar = np.asarray(im)

    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
    #print(ar.shape)

    #print((ar != chroma).shape)
    #ar = ar[not(ar == chroma).all(axis=1), :]
    #print(ar.shape)

    #print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    #print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    #print("\nCounts: ", counts , "\nCodes: " , codes)

    index_max = np.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    #print("Peak: ", peak)
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    # print('most frequent is %s (#%s)' % (peak, colour))

    r = peak[0]
    g = peak[1]
    b = peak[2]

    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('bdcolores.csv', names=index, header=None)

    minimum = 10000
    for i in range(len(csv)):
        d = abs(r - int(csv.loc[i, "R"])) + abs(g -
                                                int(csv.loc[i, "G"])) + abs(b - int(csv.loc[i, "B"]))
        # print(i)
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]

    #text = cname + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)

    print(cname)
    return cname


def Detect_Clothes_and_Crop(img_tensor, model, list_obj, image_name, txt_name, threshold=0.5):
    """Receives image tensor, image name and the txt name to write the image's labels. Detects clothes in the image using Yolo-v3 model trained on DeepFashion2 dataset. Returns a list of images with the cropped clothing items + txt with the clothing items detected."""

    img_crop_list = []

    img = np.squeeze(img_tensor.numpy())
    img_width = img.shape[1]
    img_height = img.shape[0]
    # Open file in append mode. If file does not exist, it creates a new file.
    file = open(txt_name, "a")
    file.write('\n')  # write blank line to separate images
    file.write(image_name + '\n')  # Write image name on top of image labels

    # crop out one cloth
    for obj in list_obj:
        #img_crop = None
        if obj['confidence'] > threshold:
            img_crop = img[int(obj['y1']*img_height):int(obj['y2']*img_height),
                           int(obj['x1']*img_width):int(obj['x2']*img_width), :]
            print('Item: ' + obj['label'])

        cname = Detect_Color(img_crop)

        # #if the detection's confindence is not above the threshold: 'N/A'
        # if cname=='N/A':
        #     obj['label']='N/A'

        file.write(obj['label'] + '\n' + cname + '\n')
        img_crop_list.append(img_crop)

        obj['label'] = obj['label'] + ' ' + cname

    if len(list_obj) == 1:
        file.write('N/A' + '\n' + 'N/A' + '\n')

    if not list_obj:
        file.write('N/A' + '\n' + 'N/A' + '\n' + 'N/A' + '\n' + 'N/A' + '\n')

    file.close()
    return img_crop_list


def resize_img(img_path):
    """Receives image path, returns image tensor 
        to be feeded to Detect_Clothes / Detect_Clothes_and_crop"""

    # read image
    img_original = cv2.imread(img_path)
    print('Original dimensions : ', img_original.shape)

    # resize image
    height = img_original.shape[0]
    width = img_original.shape[1]
    if (img_original.shape[0] > img_original.shape[1]):  # check if image is vertical

        if (img_original.shape[0] > 900):
            height = 900
        if (img_original.shape[1] > 750):
            width = 750
    else:  # check if image is horizontal
        if (img_original.shape[0] > 750):
            height = 750
        if (img_original.shape[1] > 900):
            width = 900

    dim = (width, height)
    img_resized = cv2.resize(img_original, dim, interpolation=cv2.INTER_AREA)
    print('Resized dimensions : ', img_resized.shape)

    # Convert image to dtype string 0-D tensor
    flag, bts = cv2.imencode('.jpg', img_resized)
    byte_arr = [bts[:, 0].tobytes()]
    tensor_string = tf.constant(byte_arr)
    tensor_string_0d = tf.reshape(tensor_string, shape=[])
    img = tf.image.decode_image(
        tensor_string_0d, channels=3, dtype=tf.dtypes.float32)
    img = tf.expand_dims(img, 0)

    return img


if __name__ == '__main__':
    """Receives the path of an image and the txt to write the labels and color, returns a .txt with the clothing items detected and their color"""
    # input = '/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets/pipo'
    # txt_name = '/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets/pipo/prueba.txt'

    # ex:'/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets/pipo'
    input = sys.argv[1]
    # ex: '/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets/pipo/prueba.txt'
    txt_name = sys.argv[2]

    if not(os.path.isdir(input)):
        print('Invalid directory')
        sys.exit()

    if os.path.exists(txt_name):
        os.remove(txt_name)
        print("Overwriting file..." + '\n')
    else:
        print("Creating file..." + '\n')

    # img_path = sys.argv[1]          # ex: './images/c5.jpg'
    # txt_name = sys.argv[2]          # ex: "label.txt"
    # aux = img_path.split('/')
    # image_name = aux[-1]            # ex: 'c5.jpg'

    model = Load_DeepFashion2_Yolov3()

    for image_name in os.scandir(input):

        img_path = input + '/' + image_name.name
        print('\n' + '\n' + 'Reading image ' + image_name.name + '...' + '\n')
        img = resize_img(img_path)

        list_obj = Detect_Clothes(img, model)
        img_cropped_list = Detect_Clothes_and_Crop(
            img, model, list_obj, image_name.name, txt_name)
        img_with_boxes = Draw_Bounding_Box(img, list_obj)

        #cv2.imshow("Clothes detection", cv2.cvtColor(img_with_boxes, cv2.COLOR_RGB2BGR))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #aux2 = image_name.name.split('.')
        #plain_name = aux2[0]
        cv2.imwrite("/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets/pipo//outfit_detected/outfit_detected_" +
                    image_name.name, cv2.cvtColor(img_with_boxes, cv2.COLOR_RGB2BGR)*255)

        # i = 1

        # for image in img_cropped_list:
        #     cv2.imwrite("./images/outfit_cropped" + str(i) + ".jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR)*255)
        #     i+=1
