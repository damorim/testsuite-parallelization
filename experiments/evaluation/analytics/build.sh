#!/bin/bash
PLOTS_DIR=plots
R --vanilla --slave < Main.R --args $1 $PLOTS_DIR

# Crop blank spaces from plots dir
for PDF in $(find $PLOTS_DIR -name "*.pdf"); do
    pdfcrop $PDF $PDF
done;
