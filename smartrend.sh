#!/bin/bash
# File that integrates all scripts

dir=./logs/$(date '+%d-%m-%Y_%Hh-%Mm')
mkdir -p $dir

# Run media scraping
node ./webscraping/media.js &> $dir/media-scraping.txt || { echo "Error: Media scraping execution failed. Logs at directory $dir"; exit 0; } 

# TODO: Run image recognition

# TODO: Run data processing

# Run retail scraping
node ./webscraping/retail.js &> $dir/retail-scraping.txt || { echo "Error: Retail scraping execution failed. Logs at directory $dir"; exit 0; }

echo Execution completed successfully

exit 1