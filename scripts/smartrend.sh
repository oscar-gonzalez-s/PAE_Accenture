#!/bin/bash
# File that integrates all scripts

# Define directories of interest
BASE_PATH=/veu4/usuaris26/pae2021/pae/PAE_Accenture
DIR_LOGS=$BASE_PATH/logs/$(date '+%d-%m-%Y_%Hh-%Mm')
DIR_ASSETS=$BASE_PATH/assets
DIR_HIST=$BASE_PATH/history # Where historical record of generated files is found.
mkdir -p $DIR_LOGS # -p no error if directory already exists
mkdir -p $DIR_HIST

# Run media scraping
echo "Scraping media images..."
# node $BASE_PATH/webscraping/media.js | tee $DIR_LOGS/media-scraping.txt
# [ ${PIPESTATUS[0]} == 1 ] && { echo "Error: Media scraping execution failed. Logs at directory $DIR_LOGS"; exit 1; }
cp $DIR_ASSETS/media-output.json $DIR_HIST/media-output_$(date '+%d_%m_%Y').json || exit 1

# Run image recognition
echo "Detecting cloth items and colours..."
bash $BASE_PATH/scripts/image_recognition_integration.sh $BASE_PATH | tee $DIR_LOGS/image-recognition.txt 
[ ${PIPESTATUS[0]} == 1 ] && { echo "Error: Image Recognition execution failed. Logs at directory $DIR_LOGS"; exit 1; }

TELE_EXIST=True
RECOG_PATH=$DIR_ASSETS/recognition-output.json
INFLU_PATH=$DIR_ASSETS/influencers.csv
TELE_HIST=$DIR_ASSETS/telegram-history.csv
TELE_DATA=$DIR_ASSETS/telegram-data.json
ITEM_REC=$DIR_ASSETS/items-record.csv
TREND_ITEM=$DIR_ASSETS/trend-items.csv
N_WEEKS=3
RELEVANC=0.1

echo "Predicting trend item of the week..."
bash $BASE_PATH/scripts/data_integration.sh $BASE_PATH $TELE_EXIST $RECOG_PATH $INFLU_PATH $TELE_HIST $TELE_DATA $ITEM_REC $TREND_ITEM $N_WEEKS $RELEVANC | tee $DIR_LOGS/data-processing.txt 
[ ${PIPESTATUS[0]} == 1 ] && { echo "Error: Data Processing execution failed. Logs at directory $DIR_LOGS"; exit 1; }

# # Run retail scraping
echo "Searching trend item on retail stores..."
node $BASE_PATH/webscraping/retail.js | tee $DIR_LOGS/retail-scraping.txt
[ ${PIPESTATUS[0]} == 1 ] && { echo "Error: Retail scraping execution failed. Logs at directory $DIR_LOGS"; exit 1; }

echo "Execution completed successfully :D"

exit 0