#!/bin/bash
#
# Utility script to crop blank spaces from pdf images
#
# Author: Jeanderson Candido
for PDF in $(find . -name *.pdf); do
    pdfcrop $PDF $PDF
done;
