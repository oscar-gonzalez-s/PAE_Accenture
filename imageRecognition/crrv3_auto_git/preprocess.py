from __future__ import print_function
import binascii
import struct
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import pandas as pd
import cv2 #openCV 
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import numpy as np
import torch
from torchvision.models.segmentation import deeplabv3_resnet101
from torchvision import transforms

def masking(image_to_transform, mask):
  width, heigh, nchannels = image_to_transform.shape
  for x in range(width):
    for y in range(heigh):
      if mask[x][y]==False:
        image_to_transform[x][y][0] = 0
        image_to_transform[x][y][1] = 177
        image_to_transform[x][y][2] = 64
  return image_to_transform
  
def apply_deeplab(deeplab, img, device):
    deeplab_preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = deeplab_preprocess(img)
    input_batch = input_tensor.unsqueeze(0)
    with torch.no_grad():
        output = deeplab(input_batch.to(device))['out'][0]
    output_predictions = output.argmax(0).cpu().numpy()
    return (output_predictions == 15)

def make_deeplab(device):
    deeplab = deeplabv3_resnet101(pretrained=True).to(device)
    deeplab.eval()
    return deeplab

def to_chroma(img):

  if (type(img).__module__ != np.__name__):
    print("wrong type")
    return 0

  k = min(1.0, 1024/max(img.shape[0], img.shape[1]))
  img = cv2.resize(img, None, fx=k, fy=k, interpolation=cv2.INTER_LANCZOS4)
  
  device = torch.device("cpu")
  deeplab = make_deeplab(device)

  mask = apply_deeplab(deeplab, img, device)

  img_final = masking(img, mask)

  return img_final