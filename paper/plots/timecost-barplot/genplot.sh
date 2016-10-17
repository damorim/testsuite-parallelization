#!/bin/bash
DATA_PATH="timecost-groups.csv"
R --vanilla < script.r --args $DATA_PATH
