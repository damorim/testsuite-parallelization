#/bin/bash
RAW_DATA_PATH=../../rawdata.csv
PLOTS_DIR=plots
if [ -z $RAW_DATA_PATH ]; then
    echo "Missing raw data path!"
    exit 1
fi

./gendata.py "$RAW_DATA_PATH" data.csv
R --vanilla < R/barplot.r --args data.csv "$PLOTS_DIR/temp"
