# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 9:34:08 2021

@author: Laura Rayón
"""

import numpy as np
import sys
import json


def contains(element, lista):
    """Checks if element is contained in list, returns true if so"""
    for i in lista:
        if i == element:
            return True
    return False


def read_txt(file_name):
    """Reads file.txt to extract image indexes, clothing items and their color.
       Returns 2D numpy array where each position corresponds to a different
       image and second array has at least 1 position, being:
       [0][0] image index (ex: 0)
       [0][1] image clothing item1 (ex: long_sleeve_top)
       [0][2] image clothing item1 color (ex: blue)
       [0][3] image clothing item2 (ex: shorts)
       [0][4] image clothing item2 color (ex: white)
    """
    # READ FILE
    f = open(file_name, "rt")       # open in read text mode

    # SAVE INFO INTO MATRIX
    # ignore first blank line
    nblancklines = -1               # #images contained in txt
    new_image = False
    matrix = []                     # matrix to store labels
    while True:
        # Get next line from file
        line = f.readline()

        # if end of file is reached
        if not line:
            break

        # decide if next line will be the start of an image
        if line == '\n':
            image = []
            nblancklines += 1
            if nblancklines > -1:
                matrix.append(image)
            new_image = True
        else:
            # if current line is the start of an image
            if new_image == True:
                # get image_index
                result1 = line.split('.')
                image_index = result1[0]
                image.append(image_index)
                new_image = False
            else:
                image.append(line.rstrip('\n'))

    f.close()
    # Decide if its an upper body item or a lower body item
    # define possible clothing items
    upper_items = ['camiseta_manga_corta', 'jersey', 'abrigo_manga_corta', 'abrigo_manga_larga', 'chaleco',
                   'top_tirantes_finos', 'vestido_manga_corta', 'vestido_manga_larga', 'vestido_de_chaleco', 'vestido_tirantes']
    lower_items = ['pantalon_corto', 'pantalones', 'falda']
   # matrix ([0-range][1-4]) clothing items, 0 is the image
    for m in range(len(matrix)):  # 0,1,2,3,4...
        # if first element is a lowerpart and second element is an upper part or an N/A
        if contains(matrix[m][1], lower_items) and (contains(matrix[m][3], upper_items) or matrix[m][3] == "N/A"):
            auxitem = matrix[m][1]
            auxcolor = matrix[m][2]
            matrix[m][1] = matrix[m][3]
            matrix[m][2] = matrix[m][4]
            matrix[m][3] = auxitem
            matrix[m][4] = auxcolor

            # if first element is a lowerpart or N/A and second element is an upper part
        elif ((contains(matrix[m][1], lower_items) or matrix[m][1] == "N/A") and contains(matrix[m][3], upper_items)):
            auxitem = matrix[m][1]
            auxcolor = matrix[m][2]
            matrix[m][1] = matrix[m][3]
            matrix[m][2] = matrix[m][4]
            matrix[m][3] = auxitem
            matrix[m][4] = auxcolor
            # if both elements are upper, delete second element
        elif (contains(matrix[m][1], upper_items) and contains(matrix[m][3], upper_items)):
            matrix[m][3] = "N/A"
            matrix[m][4] = "N/A"
            # if both elements are lower, delete first element
        elif (contains(matrix[m][1], lower_items) and contains(matrix[m][3], lower_items)):
            matrix[m][1] = "N/A"
            matrix[m][2] = "N/A"

    return nblancklines+1, matrix


def write_json(image_index, new_data, filename):
    """Receives jason, image index and data to be written there"""
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside image_index
        file_data['output'][int(image_index)].update(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


if __name__ == '__main__':
    """
    Receives: 
    - .txt with the image's name and labels found
    - .json to write them to
    Returns:
    - new modifyed .json

    **For this to work, json must contain the images 
    whose indexes are in the .txt**
    """

    txt_name = sys.argv[1]          # ex: "label.txt"
    json_file = sys.argv[2]         # ex: "media-output.json"
    # json_new = "recognition-output.json"

    # Extract information from .txt
    n_images, matrix = read_txt(txt_name)

    # Modify json with extracted information
    for i in range(n_images):  # run through all images in .txt
        nitems = int((len(matrix[i])-1)/2)  # number of clothing items in file
        image_index = int(matrix[i][0])  # index of image
        for k in range(nitems):  # run through clothing items in image
            label = str(matrix[i][1+2*k]) + ' ' + str(matrix[i][2+2*k])
            it = "item" + str(k)
            key_value = {str(it): str(label)}
            write_json(image_index, key_value, json_file)
