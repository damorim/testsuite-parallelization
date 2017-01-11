#!/bin/bash

# R --vanilla < effort.r --args  effort2.data
# mv Rplots.pdf effort2.pdf

NAME="relativeSD"
R --vanilla < ${NAME}.r

