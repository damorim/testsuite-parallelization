#!/bin/bash
PLOTS_DIR=$2
if [ ! -d "$PLOTS_DIR" ]; then
    mkdir $PLOTS_DIR
fi
R --vanilla --slave < Main.R --args $1 $PLOTS_DIR

# Crop blank spaces from plots dir
for PDF in $(find $PLOTS_DIR -name "*.pdf"); do
    pdfcrop $PDF $PDF
done;
