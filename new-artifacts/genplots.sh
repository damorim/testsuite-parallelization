#!/bin/bash
#
# This script generates the PDF plots.
# Author: Jeanderson Candido <http://jeandersonbc.github.io>
#
BASEDIR="`pwd`"

RSCRIPTS=(
    subjects.r
    rq1.r
    rq2.r
    rq4.r
)

for rscript in ${RSCRIPTS[@]}; do
    R --vanilla --quiet --slave < $BASEDIR/src/plots/$rscript
done
for plot in `ls | grep .pdf`; do
    pdfcrop $plot $plot &>/dev/null
    done;
