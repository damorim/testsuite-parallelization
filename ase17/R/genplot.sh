#!/bin/bash

NAME="testcost"
Rscript --vanilla ${NAME}.r "testcost-med"
Rscript --vanilla ${NAME}.r "testcost-long"

