#!/bin/bash
DATA_PATH="timetests-data.csv"
R --vanilla < script.r --args $DATA_PATH
