#!/bin/bash
INPUT=$1

CODE=$(echo $INPUT | sed "s/.*-//g" | sed "s/.csv//g")
PLOTS_DIR=results/$CODE
if [ ! -d "$PLOTS_DIR" ]; then
    mkdir $PLOTS_DIR
fi
R --vanilla --slave < Helper.R --args $INPUT $PLOTS_DIR

# Crop blank spaces from plots dir
for PDF in $(find $PLOTS_DIR -name "*.pdf"); do
    pdfcrop $PDF $PDF
done;

pdftk $(find $PLOTS_DIR -name "*.pdf") cat output summary-$CODE.pdf
