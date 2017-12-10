#!/bin/bash

Rscript --vanilla scalability.r
pdfcrop scalability.pdf scalability.pdf
