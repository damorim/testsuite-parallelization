#!/bin/bash
R --vanilla --slave < Sanity.R
R --vanilla --slave < Main.R

# Crop blank spaces from plots dir
PLOTS_DIR=plots
for PDF in $(find $PLOTS_DIR -name "*.pdf"); do
    pdfcrop $PDF $PDF
done;
