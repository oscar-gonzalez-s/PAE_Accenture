#!/bin/bash

#Call cloth_detection.py for each image of specified folder as script's argument

GETF0="cloth_detection.py"
READ_FILE="/veu4/usuaris26/pae2021/crrv3_auto/imgs"
LABEL_TXT="label_prueba.txt"

NUMBER_OF_FILES=$(ls $READ_FILE | wc -l)


#for i in $(seq 1 1 $NUMBER_OF_FILES); do
#     $(expr $i - 1)
#done

for img in /veu4/usuaris26/pae2021/crrv3_auto/imgs/*.jpg; do
    python3 $GETF0 $img $LABEL_TXT > /dev/null || (echo "Error in $GETF0 $img $LABEL_TXT"; exit 1)
done


