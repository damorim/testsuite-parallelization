#!/bin/bash
#
# This script run sequential programs to generates data for the RQ1


# generate csv file with dataset details from test reports
# It's necessary the directory ./reports with the test reports 
./parse-rawdata.py 

R --vanilla --quiet --slave < ./summarize.r

#./sanitizer.py 3 10.0

#./parse-testcases.py

#R ./rq1.r
