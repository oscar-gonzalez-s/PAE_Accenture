#!/bin/bash
# Needs as argument the directory to retrieve images to process 
#ex: "/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets"

GETF0="cloth_detection.py"
GETF1="json_edit.py"

# CALL TO CLOTH_DETECTION.PY
DIR_NAME="/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets" #$1
INPUT=$DIR_NAME/pipo #in final implementation dir will be 'instaImages'
LABEL_TXT=$DIR_NAME/labels_$(date '+%d_%m_%Y').txt
#input = sys.argv[1]          # ex:'/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets/pipo'
#txt_name = sys.argv[2]          # ex: '/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets/pipo/prueba.txt'
python3 $GETF0 $INPUT $LABEL_TXT > /dev/null || (echo "Error in $GETF0 $INPUT $LABEL_TXT"; exit 0)

# CALL TO JSON_EDIT.PY
#txt_name = sys.argv[1]          # ex: "label.txt"
#json_file = sys.argv[2]         # ex: "media-output.json"
#Create json copy to store label info 
RECOG=$DIR_NAME/recognition-test_$(date '+%d_%m_%Y').json
MEDIA=$DIR_NAME/media-test.json
cp $MEDIA $RECOG || (echo "Error in copying media-output.json"; exit 0)
python3 $GETF1 $LABEL_TXT $RECOG > /dev/null || (echo "Error in $GETF1 $LABEL_TXT $RECOG"; exit 0)
