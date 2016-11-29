#!/usr/bin/env bash
#
# Execute scripts with test parameters
# Author: Jeanderson Candido
#
BASEDIR=..
RESOURCES_DIR=$BASEDIR/test/data/
PYSOURCES=$BASEDIR/py
./$PYSOURCES/downloader.py "$RESOURCES_DIR/download-test.csv" --output "$RESOURCES_DIR/verified-subjects.csv"