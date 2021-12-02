#!/bin/bash
# File that integrates all scripts

dir=./logs/$(date '+%d-%m-%Y_%Hh-%Mm')
mkdir -p $dir # -p no error if directory already exists

# Define directories of interest
BASE_PATH="/veu4/usuaris26/pae2021/pae/PAE_Accenture"
DIR_ASSETS=$BASE_PATH/assets
DIR_HIST=$BASE_PATH/history # Where historical record of generated files is found.
mkdir -p $DIR_HIST
# Run media scraping
node ./webscraping/media.js &> $dir/media-scraping.txt || { echo "Error: Media scraping execution failed. Logs at directory $dir"; exit 0; } 
mv $DIR_ASSETS/media-output.json $DIR_HIST/media-output_$(date '+%d_%m_%Y').json

# Run image recognition
sh image_recognition_integration.sh $DIR_ASSETS $DIR_HIST &> $dir/image-recognition.txt || { echo "Error: Image Recognition execution failed. Logs at directory $dir"; exit 0; }

# TODO: Run data processing
TELE_EXIST=True
RECOG_PATH=$DIR_ASSETS/recognition-output.json
INFLU_PATH=$DIR_ASSETS/influencers.csv
TELE_HIST=$DIR_ASSETS/telegram-history.csv
TELE_DATA=$DIR_ASSETS/telegram-data.json
ITEM_REC=$DIR_ASSETS/items-record.csv
TREND_ITEM=$DIR_ASSETS/trend-items.csv
N_WEEKS=3
RELEVANC=0.1

sh data_integration.sh $BASE_PATH $TELE_EXIST $RECOG_PATH $INFLU_PATH $TELE_HIST $TELE_DATA $ITEM_REC $TREND_ITEM

# Run retail scraping
node ./webscraping/retail.js &> $dir/retail-scraping.txt || { echo "Error: Retail scraping execution failed. Logs at directory $dir"; exit 0; }

echo Execution completed successfully

exit 1