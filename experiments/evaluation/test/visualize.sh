#!/usr/bin/env bash
BASEDIR=..
OUTPUT_DIR=$BASEDIR/test/gen
RSOURCES=$BASEDIR/analytics
R --vanilla --slave < ./$RSOURCES/Main.R --args $1 $OUTPUT_DIR
