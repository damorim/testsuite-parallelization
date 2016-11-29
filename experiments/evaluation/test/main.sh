#!/usr/bin/env bash
#
# Execute scripts with test parameters
# Author: Jeanderson Candido
#
BASEDIR=..
RESOURCES_DIR=$BASEDIR/test/data/
OUTPUT_DIR=$BASEDIR/test/gen/
PYSOURCES=$BASEDIR/py
./$PYSOURCES/main.py "$RESOURCES_DIR/verified-subjects.csv" -d $OUTPUT_DIR $1
