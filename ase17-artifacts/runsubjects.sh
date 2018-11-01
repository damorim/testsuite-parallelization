#!/bin/bash
#
# This script generates data for the following sections: subjects,
# rq1, and rq2
#
# Author: Jeanderson Candido <http://jeandersonbc.github.io>
#
SCRIPTS=./src
PROJECTS_DIR=./projects/downloads
OUTPUT_DIR=./rawdata
RERUNS=3

#echo "Started at `date`" >> runs.txt
#for run in `seq 1 $RERUNS`; do
#    $SCRIPTS/compile-test.sh 90m $PROJECTS_DIR $OUTPUT_DIR && echo "Finished run #$RERUNS at `date`" >> runs.txt
#done

#$SCRIPTS/parse-rawdata.py $OUTPUT_DIR
R --vanilla --quiet --slave < $SCRIPTS/summarize.r
$SCRIPTS/sanitizer.py 3 10.0
$SCRIPTS/parse-testcases.py
