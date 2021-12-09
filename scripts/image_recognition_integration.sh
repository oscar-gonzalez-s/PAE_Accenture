#!/bin/bash
# Needs as argument the directory to retrieve images to process 
# And the directory to store the historical copies 
#ex: "/veu4/usuaris26/pae2021/pae/PAE_Accenture-imageRecognition/assets"

# HELP DEFINITION
if [ "$1" == "-h" ] ; then
    echo "Entrance variables: "
    echo "\$1 = working path"
    exit 1
fi

BASE_PATH=$1 #/veu4/usuaris26/pae2021/pae/PAE_Accenture
DIR_NAME=$BASE_PATH/assets
DIR_HIST=$BASE_PATH/history

GETF0="$BASE_PATH/imageRecognition/crrv3_auto_git/cloth_detection.py"
GETF1="$BASE_PATH/imageRecognition/crrv3_auto_git/json_edit.py"

# CALL TO CLOTH_DETECTION.PY
INPUT=$DIR_NAME/instaImages #in final implementation dir will be 'instaImages'
LABEL_TXT=$DIR_NAME/labels.txt
echo "Executing cloth_detection.py..."
python3 $GETF0 $BASE_PATH $INPUT $LABEL_TXT || (echo "Error in $GETF0 $INPUT $LABEL_TXT"; exit 1)

# CALL TO JSON_EDIT.PY
#Create json copy to store label info 
RECOG=$DIR_NAME/recognition-output.json
MEDIA=$DIR_NAME/media-output.json
cp $MEDIA $RECOG || (echo "Error in copying media-output.json"; exit 1)
echo "Executing json_edit.py..."
python3 $GETF1 $LABEL_TXT $RECOG > /dev/null || (echo "Error in $GETF1 $LABEL_TXT $RECOG"; exit 1)
# Implementar histórico en carpeta externa
cp $LABEL_TXT $DIR_HIST/labels_$(date '+%d_%m_%Y').json & cp $RECOG $DIR_HIST/recognition-output_$(date '+%d_%m_%Y').json
