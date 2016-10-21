#!/bin/bash
RAW_DATA_PATH=../../rawdata.csv
PLOTS_DIR=plots
if [ -z $RAW_DATA_PATH ]; then
    echo "Missing raw data path!"
    exit 1
fi

./gendata.py "$RAW_DATA_PATH" data.csv

R --vanilla < R/barplot.r --args data.csv "$PLOTS_DIR/barplot-timecost"

R --vanilla < R/scatter.r --args data.csv "Normal" "$PLOTS_DIR/scatterplot-norm"
R --vanilla < R/scatter.r --args data.csv "Long" "$PLOTS_DIR/scatterplot-long"
R --vanilla < R/scatter.r --args data.csv "Very Long" "$PLOTS_DIR/scatterplot-vlong"

