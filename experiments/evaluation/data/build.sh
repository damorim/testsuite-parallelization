#!/bin/bash
PROBLEMS=$(R --vanilla --slave < Sanity.R)
if [[ ! -z $PROBLEMS ]]; then
    echo "Dataset is inconsistent"
    echo $PROBLEMS | sed "s/\"\|\[[0-9]*\] //g"
    exit
fi
R --vanilla < Main.R

# Crop blank spaces from plots dir
PLOTS_DIR=plots
for PDF in $(find $PLOTS_DIR -name "*.pdf"); do
    pdfcrop $PDF $PDF
done;
