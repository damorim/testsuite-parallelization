#!/bin/bash
BASEDIR=$(pwd)
for d in $(ls .); do
    if [ -f "$d/main.sh" ]; then
        cd $d
        ./main.sh
        cd $BASEDIR
    fi
done

# Crop blank spaces
for PDF in $(find . -name *.pdf); do
    pdfcrop --margins '3 3 3 3' $PDF $PDF
done;
