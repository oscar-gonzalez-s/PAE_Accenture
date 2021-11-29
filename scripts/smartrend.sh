#!/bin/bash
# File that integrates all scripts

dir=./logs/$(date '+%d-%m-%Y_%Hh-%Mm')
mkdir -p $dir # -p no error if directory already exists

# Define directories of interest
DIR_ASSETS="/veu4/usuaris26/pae2021/pae/PAE_Accenture/assets"
DIR_HIST = "/veu4/usuaris26/pae2021/pae/PAE_Accenture/history"

# Run media scraping
node ./webscraping/media.js &> $dir/media-scraping.txt || { echo "Error: Media scraping execution failed. Logs at directory $dir"; exit 0; } 
mv $DIR_ASSETS/media-output.json $DIR_HIST/media-output_$(date '+%d_%m_%Y').json

# Run image recognition
./image_recognition_integration.sh $DIR_ASSETS $DIR_HIST &> $dir/image-recognition.txt || { echo "Error: Image Recognition execution failed. Logs at directory $dir"; exit 0; }

# TODO: Run data processing

# Run retail scraping
node ./webscraping/retail.js &> $dir/retail-scraping.txt || { echo "Error: Retail scraping execution failed. Logs at directory $dir"; exit 0; }

echo Execution completed successfully

exit 1