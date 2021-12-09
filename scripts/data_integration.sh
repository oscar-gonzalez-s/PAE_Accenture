#!/bin/bash

# HELP DEFINITION
if [ "$1" == "-h" ] ; then
    echo "Entrance variables: "
    echo "\$1 = working path. Ex:'/veu4/usuaris26/pae2021/pae/PAE_Accenture'."
    echo "\$2 = boolean to indicate if a telegram-data.json has been generated"
    echo "\$3 = path to recognition-output.json"
    echo "\$4 = path to influencers.csv"
    echo "\$5 = path to telegram-history.csv"
    echo "\$6 = path to telegram-data.json"
    echo "\$7 = path to items-record.csv"
    echo "\$8 = path to trend-items.csv"
    echo "\$9 = parameter to determine the number of weeks that are taken into account for trend evolution. Default value = 3"
    echo "\$10 = parameter to determine the relevance Telegram results have on the calculus of the influencer score. Default value = 0"
    exit 0
fi
# Needs as argument the directory to execute data analysis main process 
GETF0="$1/DataProcessing/main.py"

# CALL TO MAIN.PY
python3 $GETF0 $2 $3 $4 $5 $6 $7 $8 $9 ${10} || (echo "Error in $GETF0 $INPUT $LABEL_TXT"; exit 1)