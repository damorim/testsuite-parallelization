#!/bin/bash
BASEDIR=$(pwd)
for d in $(ls .); do
    if [ -f "$d/main.sh" ]; then
        cd $d
        ./main.sh
        cd $BASEDIR
    fi
done

# TODO: Move pdfcrop calls to R scripts so I can use
#       different margins
#
# Crop blank spaces
for PDF in $(find . -name *.pdf); do
    pdfcrop $PDF $PDF
done;
