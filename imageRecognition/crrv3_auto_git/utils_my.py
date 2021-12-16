# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 16:14:17 2019

@author: fonollosa (Berlin)
"""

import numpy as np
import time
import tensorflow as tf
import cv2

from yolov3_tf2.models import YoloV3


def Draw_Bounding_Box(img, list_obj):
    try:
        img = img.numpy() # convert tensor to numpy array
    except:
        pass

    img = np.squeeze(img)

    img_width = img.shape[1]
    img_height = img.shape[0]

    # color_yellow = [244/255, 241/255, 66/255]
    # color_green = [66/255, 241/255, 66/255]
    # color_red = [241/255, 66/255, 66/255]
    # color_blue = [66/255, 66/255, 241/255]

    color_yellow = [253/255, 255/255, 50/255]
    color_green = [140/255, 255/255, 50/255]
    color_red = [255/255, 7/255, 58/255]
    color_blue = [13/255, 213/255, 252/255]

    # draw rectangle bounding box for cars
    for obj in list_obj:
        x1 = int(round(obj['x1']*img_width))
        y1 = int(round(obj['y1']*img_height))
        x2 = int(round(obj['x2']*img_width))
        y2 = int(round(obj['y2']*img_height))

        if 'camiseta_manga_corta' in obj['label']:
            color = color_yellow
        elif 'pantalones' in obj['label'] :
            color = color_red
        elif 'camiseta_manga_larga' in obj['label'] :
            color = color_blue
        else:
            color = color_green
        # if obj['label'] == 'short_sleeve_top':
        #     color = color_yellow
        # elif obj['label'] == 'trousers':
        #     color = color_red
        # else:
        #     color = color_green
                
        # text = '{}: {:.2f}'.format(obj['label'], obj['confidence'])
        # img = cv2.rectangle(img, (x1, y1), (x2, y2), color, 4)
        # img = cv2.putText(img, text, (x1, y1-5), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2, cv2.LINE_AA)
        
        aux = obj['label'].split(' ')
        
        aux2 = aux.copy()
        aux2.pop(0)

        #text = '{}: {:.2f}'.format(obj['label'], obj['confidence'])

        text = '{} ({:.2f}) {}'.format(aux[0], obj['confidence'], ' '.join(aux2))

        # draw bounding box and centered labels
        letter_size = 12
        box_length = x2-x1
        label_length = len(text)*letter_size

        if (label_length < box_length):
            x = x1+int((box_length-label_length)/2)
        else:
        #    x = x1-int(0.25*letter_size*len(text))
            x = x1-int((label_length-box_length)/2)
        
        
        img = cv2.rectangle(img, (x1, y1), (x2, y2), color, 4)
        img = cv2.putText(img, text, (x, y1-10), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2, cv2.LINE_AA)

        

    return img

def Read_Img_2_Tensor(img_path):
    img_raw = tf.io.read_file(img_path)
    img = tf.image.decode_image(img_raw, channels=3, dtype=tf.dtypes.float32)
    img = tf.expand_dims(img, 0) # fake a batch axis

    return img

def Load_DeepFashion2_Yolov3(base_path):
    weights_path = base_path + '/imageRecognition/crrv3_auto_git/built_model/deepfashion2_yolov3'
    t1 = time.time()
    model = YoloV3(classes=13)
    model.load_weights(weights_path)
    t2 = time.time()
    print('Load DeepFashion2 Yolo-v3 from disk: {:.2f} sec'.format(t2 - t1))

    return model

def Save_Image(image_array, save_path):
    if image_array.dtype == 'float32':
        cv2.imwrite(save_path, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)*255)
    elif image_array.dtype == 'uint8':
        cv2.imwrite(save_path, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))
    else:
        raise ValueError('Unrecognize type of image array: {}', image_array.dtype)
