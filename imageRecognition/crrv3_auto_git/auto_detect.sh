#!/bin/bash

#Call cloth_detection.py for each image of specified folder as script's argument

GETF0="cloth_detection.py"
READ_FILE="/veu4/usuaris26/pae2021/pae/PAE_Accenture/imageRecognition/crrv3_auto_git/imgs"
LABEL_TXT="label_prueba.txt"

#NUMBER_OF_FILES=$(ls $READ_FILE | wc -l)
#for i in $(seq 1 1 $NUMBER_OF_FILES); do
#     $(expr $i - 1)
#done

#if LABEL_TXT files exist, we will remove it
if [ -f "$LABEL_TXT" ]
then
    rm $LABEL_TXT
fi


for img in /veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/imageRecognition/crrv3_auto_git/imgs/*.jpg; do
    python3 $GETF0 $img $LABEL_TXT > /dev/null || (echo "Error in $GETF0 $img $LABEL_TXT"; exit 1)
done