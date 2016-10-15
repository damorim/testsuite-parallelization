#!/bin/bash
RAW_DATA_PATH=../../../experiments/test-regression-cost-eval/timecost.csv
if [ -z $RAW_DATA_PATH ]; then
    echo "Missing raw data path!"
    exit 1
fi
./gendata.py "$RAW_DATA_PATH"
./genplot.sh "timecost-groups.csv"
