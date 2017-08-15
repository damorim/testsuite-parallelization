#!/bin/bash
for f in `ls | grep pdf`; do pdfcrop $f $f; done;
