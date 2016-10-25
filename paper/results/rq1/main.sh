#!/bin/bash
RAW_DATA_PATH=../rawdata.csv
PLOTS_DIR=plots
if [ -z $RAW_DATA_PATH ]; then
    echo "Missing raw data path!"
    exit 1
fi

./gendata.py "$RAW_DATA_PATH" data.csv

# Replaced by the piechart
#R --vanilla < R/barplot.r --args data.csv "$PLOTS_DIR/barplot-timecost"

R --vanilla < R/scatter.r --args data.csv "Medium" "$PLOTS_DIR/scatterplot-med"
R --vanilla < R/scatter.r --args data.csv "Long" "$PLOTS_DIR/scatterplot-long"

R --vanilla < R/piechart.r --args data.csv "$PLOTS_DIR/piechart"

